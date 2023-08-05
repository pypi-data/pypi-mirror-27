# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Helper classes for runtime storage."""

import threading

import pkg_resources

from .utils import HAS_ASYNCIO

if HAS_ASYNCIO:
    from . import async_context


class _BaseRuntimeStorage(object):
    """Base class for runtime storage objects.

    Subclasses must define a store attribute.
    """

    def store_request(self, request):
        """Store a request."""
        self.store.set('current_request', request)
        self.store.delete('whitelist_match')

    def store_request_default(self, request):
        """Store a request, unless a request is already stored."""
        self.store.setdefault('current_request', request)
        self.store.delete('whitelist_match')

    def clear_request(self):
        """Clear the stored request."""
        self.store.delete('current_request')

    def get_current_request(self):
        """Return the request currently processed.

        Return None if no request is stored.
        """
        return self.store.get('current_request')

    def get_whitelist_match(self, runner_settings):
        """Return the whitelisted path or IP matching the current request.

        Return None if the request is not whitelisted.
        """
        # None is a valid value, so let's default to False when not defined.
        whitelist_match = self.store.get('whitelist_match', False)
        if whitelist_match is not False:
            return whitelist_match
        current_request = self.get_current_request()
        if current_request is None:
            whitelist_match = None
        else:
            whitelist_match = runner_settings.whitelist_match(current_request)
        self.store.set('whitelist_match', whitelist_match)
        return whitelist_match

    def store_current_args(self, binding_accessor):
        """For daemon only: store the faked list of arguments."""
        args = {}
        for name, value in binding_accessor.items():
            if name.find("#.args[") == 0:
                idx = int(name[7:name.rindex("]")])
                args[idx] = value
            elif name.find("#.cargs[") == 0:
                idx = int(name[8:name.rindex("]")])
                args[idx] = value
        if args:
            self.store.set('arguments',
                           [args.get(i) for i in range(max(args) + 1)])
        else:
            self.store.set('arguments', [])

    def get_current_args(self, args=None):
        """For daemon only: get the faked list of arguments."""
        return self.store.get('arguments', args)


class _ThreadLocalStore(object):
    """Wrap a threading.local object into a store interface."""

    def __init__(self):
        self.local = threading.local()

    def get(self, key, default=None):
        """Return the value associated to the key.

        Fallback to default if the key is missing.
        """
        return getattr(self.local, key, default)

    def set(self, key, value):
        """Map a key to a value."""
        setattr(self.local, key, value)

    def setdefault(self, key, value):
        """If a key is not set, map it to a value."""
        self.local.__dict__.setdefault(key, value)

    def delete(self, key):
        """Delete a key."""
        return self.local.__dict__.pop(key, None)


class ThreadRuntimeStorage(_BaseRuntimeStorage):
    """Thread-local storage for runtime information, e.g. current request.

    All supported operations are thread-safe.
    """

    def __init__(self):
        self.store = _ThreadLocalStore()


class AsyncIORuntimeStorage(_BaseRuntimeStorage):
    """Async contextual storage for runtime information, e.g. current request.

    This class is used by web frameworks based on asyncio rather than
    threading, such as aiohttp.
    """

    def __init__(self):
        self.store = async_context


_THREADED_FRAMEWORKS = (
    'Django',
    'Flask',
    'pyramid',
)

_ASYNC_FRAMEWORKS = (
    'aiohttp',
)


def get_runtime_storage():
    """Return a runtime storage instance suited for the current framework."""
    if HAS_ASYNCIO:
        pkg_names = set(pkg_info.project_name
                        for pkg_info in pkg_resources.working_set)
        for framework in _THREADED_FRAMEWORKS:
            if framework in pkg_names:
                return ThreadRuntimeStorage()
        for framework in _ASYNC_FRAMEWORKS:
            if framework in pkg_names:
                return AsyncIORuntimeStorage()
    return ThreadRuntimeStorage()


runtime = get_runtime_storage()
