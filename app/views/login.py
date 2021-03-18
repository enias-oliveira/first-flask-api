#!/usr/bin/env python3

from flask import Blueprint, request
from http import HTTPStatus
from environs import Env

from app.models.users_model import UsersModel


login = Blueprint("login", __name__)

env = Env()
env.read_env()

FILENAME = "data/users.csv" if env("TEST") != "true" else "data/users_test.csv"


@login.route("/login", methods=["POST"])
def login_index():
    user_credentials = request.get_json()
    users = UsersModel(FILENAME)

    logged_user = users.login(user_credentials)

    if not logged_user:
        return logged_user, HTTPStatus.UNAUTHORIZED

    return logged_user, HTTPStatus.OK
