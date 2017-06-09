# -*- coding: utf-8 -*-
"""
    tz для adcombo
"""
from flask import Flask
from blueprints.base import bp


def create_app(config=None):
    app = Flask('tz')

    app.config.update(dict(
        SECRET_KEY='development key',
    ))
    app.config.update(config or {})
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    app.register_blueprint(bp)
    return app

app = create_app()
