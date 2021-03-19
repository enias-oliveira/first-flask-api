#!/usr/bin/env python3

from flask import Blueprint, jsonify
from http import HTTPStatus
from environs import Env

from app.models.users_model import UsersModel


users_bp = Blueprint("users_bp", __name__)

env = Env()
env.read_env()

FILENAME = "data/users.csv" if env("TEST") != "true" else "data/users_test.csv"


@users_bp.route("/users")
def all_users():
    users = UsersModel(FILENAME)
    protected_users = users.get_all_users_safe()
    return jsonify(protected_users), HTTPStatus.OK
