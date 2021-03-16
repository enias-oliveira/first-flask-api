#!/usr/bin/env python3

from pytest import fixture

import csv

from app.models.users_model import UsersModel


@fixture
def users_model(tmp_path):
    users_filename = tmp_path / "users.csv"
    return UsersModel(users_filename), users_filename


@fixture
def standard_user():
    return {
        "name": "Naruto Uzumaki",
        "email": "naruto@konoha.com",
        "password": "imgoingtobeahokage123",
        "age": 19,
    }


def test_first_standard_user_signup_csv_data_output(users_model: tuple, standard_user):
    expected_first_user = {
        "id": "1",
        "name": "Naruto Uzumaki",
        "email": "naruto@konoha.com",
        "password": "imgoingtobeahokage123",
        "age": "19",
    }

    users, filename = users_model
    users.signup(standard_user)

    with open(filename, "r") as readable_file:
        reader = csv.DictReader(readable_file)
        actual_first_user = list(reader)[0]

    assert actual_first_user == expected_first_user


def test_second_user_signup_csv_data_output(users_model: tuple, standard_user):
    second_standard_user = {
        "name": "John Cena",
        "email": "john_cena@wwe.com",
        "password": "thechamp",
        "age": 40,
    }

    expected_second_user = {
        "id": "2",
        "name": "John Cena",
        "email": "john_cena@wwe.com",
        "password": "thechamp",
        "age": "40",
    }

    users, filename = users_model
    users.signup(standard_user)
    users.signup(second_standard_user)

    with open(filename, "r") as readable_file:
        reader = csv.DictReader(readable_file)
        actual_second_user = list(reader)[1]

    assert actual_second_user == expected_second_user
