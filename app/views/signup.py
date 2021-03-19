#!/usr/bin/env python3

from flask import Blueprint, request
from http import HTTPStatus
from environs import Env

from app.models.users_model import UsersModel


signup_bp = Blueprint("signup_bp", __name__)

env = Env()
env.read_env()

FILENAME = "data/users.csv" if env("TEST") != "true" else "data/users_test.csv"


@signup_bp.route("/signup", methods=["POST"])
def signup():
    request_user = request.get_json()

    users = UsersModel(FILENAME)
    created_user = users.signup(request_user)

    if not created_user:
        return {}, HTTPStatus.UNPROCESSABLE_ENTITY

    else:
        return created_user, HTTPStatus.CREATED
