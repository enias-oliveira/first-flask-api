__version__ = "0.1.0"

from flask import Flask
from environs import Env

from app import views


def create_app():
    app = Flask(__name__)

    views.init_app(app)

    env = Env()
    env.read_env()

    @app.route("/")
    def home():
        return "Hello World"

    return app
