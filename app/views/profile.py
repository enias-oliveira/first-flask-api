#!/usr/bin/env python3

from flask import Blueprint, request
from http import HTTPStatus
from environs import Env

from app.models.users_model import UsersModel


profile = Blueprint("profile", __name__, url_prefix="/profile")

env = Env()
env.read_env()

FILENAME = "data/users.csv" if env("TEST") != "true" else "data/users_test.csv"


@profile.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    patch_items = request.get_json()
    users = UsersModel(FILENAME)

    patched_user = users.update_user(user_id, **patch_items)

    return patched_user, HTTPStatus.OK


@profile.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    users = UsersModel(FILENAME)

    if users.delete(user_id):
        return "", HTTPStatus.NO_CONTENT
    else:
        return {
            "message": HTTPStatus.UNPROCESSABLE_ENTITY.phrase
        }, HTTPStatus.UNPROCESSABLE_ENTITY
