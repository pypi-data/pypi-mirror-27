# -*- coding: utf-8 -*-
# Flask-Diamond (c) Ian Dennis Miller

from flask_assets import Environment

assets = Environment()


def init_webassets(self, asset_map=None):
    """
    Initialize web assets.

    :returns: None

    `webassets <https://github.com/miracle2k/webassets>`_ make it simpler
    to process and bundle CSS and Javascript assets.  This can be baked
    into a Flask application using
    `Flask-Assets <http://flask-assets.readthedocs.org/en/latest/>`_
    """

    assets.init_app(self.app)
    if asset_map:
        asset_map(assets)
