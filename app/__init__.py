__version__ = "0.1.0"

from flask import Flask
from environs import Env


def create_app():
    app = Flask(__name__)

    env = Env()
    env.read_env()

    @app.route("/")
    def home():
        return "Hello World"

    return app
