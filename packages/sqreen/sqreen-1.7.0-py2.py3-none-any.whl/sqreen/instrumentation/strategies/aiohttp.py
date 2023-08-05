# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Strategy classes for aiohttp."""

from logging import getLogger

from ..middlewares import AioHTTPMiddleware
from .framework import FrameworkStrategy
from .import_hook import ImportHookStrategy

LOGGER = getLogger(__name__)


class AioHTTPInstallStrategy(ImportHookStrategy):
    """Wrap aiohttp.web::Application.freeze to install a custom middleware."""

    def import_hook_callback(self, original):

        def app_freeze(app):
            if AioHTTPMiddleware.handle in app._middlewares:
                # Prevents inserting the middleware twice.
                LOGGER.warning("Custom middleware already set, skipped")
            else:
                LOGGER.info("Injecting custom middleware")
                app._middlewares.insert(0, AioHTTPMiddleware.handle)
            return original(app)

        return app_freeze


class AioHTTPHookStrategy(FrameworkStrategy):
    """Hook aiohttp custom middleware."""

    MODULE_NAME = "sqreen.instrumentation.middlewares.aiohttp_middleware"
    HOOK_CLASS = "AioHTTPMiddleware"
    HOOK_METHOD = "handle"

    def __init__(self, strategy_key, observation_queue, queue,
                 import_hook, before_hook_point=None):
        super(AioHTTPHookStrategy, self).__init__(
            strategy_key, observation_queue, queue,
            import_hook, before_hook_point,
        )
        self.middleware = AioHTTPMiddleware(self, observation_queue, queue)
        self.wrapper = self._apply_middleware

    @staticmethod
    def _apply_middleware(original, middleware):
        return middleware(original)
