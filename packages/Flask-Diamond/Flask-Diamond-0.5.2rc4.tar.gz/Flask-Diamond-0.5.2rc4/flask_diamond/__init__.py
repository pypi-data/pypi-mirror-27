# -*- coding: utf-8 -*-
# Flask-Diamond (c) Ian Dennis Miller

import flask
from .facets import *

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

application = None


class Diamond:
    """
    A Diamond application.

    :param app: a Flask app that you created on your own
    :type app: Flask
    :returns: None
    """

    def __init__(self, name=None):
        """
        Initialize a Diamond application.

        :param app: a Flask app that you created on your own
        :type app: Flask
        :returns: Flask -- the initialized application object

        This function is the backbone of every Diamond application.  It will
        initialize every component of the application.  To control the
        behaviour of the initialization process, override these functions
        within your own application.
        """

        if not name:
            name = __name__

        self.app = flask.Flask(name)

        if hasattr(self.app, 'teardown_appcontext'):
            self.app.teardown_appcontext(self.teardown)
        else:
            self.app.teardown_request(self.teardown)

    def facet(self, extension_name, *args, **kwargs):
        """
        initialize an extension
        """
        init_method = "init_{0}".format(extension_name)
        if not hasattr(self, init_method):
            method_to_call = globals()[init_method]
        else:
            method_to_call = getattr(self, init_method)
        setattr(self, init_method, method_to_call)

        try:
            # try to explicitly pass self as the first parameter
            result = method_to_call(self, *args, **kwargs)
        except TypeError:
            # just call it because it will be wrapped to inject self
            result = method_to_call(*args, **kwargs)

        self.app.logger.debug("facet {0}".format(extension_name))
        return result

    def super(self, extension_name, *args, **kwargs):
        """
        invoke the initialization method for the superclass

        ex: self.super("administration")
        """

        init_method = "init_{0}".format(extension_name)
        # ensure the global version is called
        method_to_call = globals()[init_method]
        result = method_to_call(self, *args, **kwargs)
        return result

    def teardown(self, exception):
        """
        Remove any persistent connections during application context teardown.

        :returns: None
        """

        ctx = stack.top
        if hasattr(ctx, 'diamond'):
            pass
            # ctx.sqlite3_db.close()

    @property
    def _app(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'app'):
                pass
            return ctx.app
