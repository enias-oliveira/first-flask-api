#!/usr/bin/env python3

from flask import Flask


def init_app(app: Flask):
    from .signup import signup_bp
    from .login import login_bp
    from .profile import profile
    from .users import users_bp

    app.register_blueprint(signup_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(profile)
    app.register_blueprint(users_bp)
