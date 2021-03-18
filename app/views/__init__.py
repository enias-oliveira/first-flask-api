#!/usr/bin/env python3

from flask import Flask


def init_app(app: Flask):
    from .signup import signup
    from .login import login
    from .profile import profile

    app.register_blueprint(signup)
    app.register_blueprint(login)
    app.register_blueprint(profile)
