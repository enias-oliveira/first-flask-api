#!/usr/bin/env python3

from flask import Blueprint

signup = Blueprint("signup", __name__)


@signup.route("/signup", methods=["POST"])
def signup_index():
    return "Batata"
