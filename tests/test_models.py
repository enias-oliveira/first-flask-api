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


class TestUserModel:
    def test_init_attributest(self, users_model):
        users, filename = users_model
        assert users.filename == filename

    def test_first_standard_user_signup_csv_data_output(
        self, users_model: tuple, standard_user
    ):
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

    def test_second_user_signup_csv_data_output(
        self, users_model: tuple, standard_user
    ):
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

    def test_login_valid_credentials(self, users_model, standard_user):
        users, filename = users_model
        users.signup(standard_user)

        given = {"email": "naruto@konoha.com", "password": "imgoingtobeahokage123"}

        expected_response = {
            "id": "1",
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "age": 19,
        }

        actual_response = users.login(given)

        assert actual_response == expected_response

    def test_is_email_registered(self, users_model, standard_user):
        users, filename = users_model

        expected_when_csv_empty = False
        actual_when_csv_empty = users._is_email_registered(standard_user["email"])

        assert actual_when_csv_empty == expected_when_csv_empty

        users.signup(standard_user)
        expected_when_email_registered = True
        actual_when_email_registered = users._is_email_registered(
            standard_user["email"]
        )

        assert actual_when_email_registered == expected_when_email_registered

        expected_when_csv_not_empty_and_email_not_registered = False
        actual_when_csv_not_empty_and_email_not_registered = users._is_email_registered(
            "john@teste.com"
        )

        assert (
            actual_when_csv_not_empty_and_email_not_registered
            == expected_when_csv_not_empty_and_email_not_registered
        )

    def test_get_new_id(self, users_model, standard_user):
        users, filename = users_model

        expected_with_no_users_in_csv = 1
        actual_with_no_users_in_csv = users._get_new_id()

        assert actual_with_no_users_in_csv == expected_with_no_users_in_csv

        users.signup(standard_user)

        expected_with_one_user_in_csv = 2
        actual_with_one_user_in_csv = users._get_new_id()

        assert actual_with_one_user_in_csv == expected_with_one_user_in_csv

    def test_get_all_users(self, users_model, standard_user):
        users, filename = users_model

        expected_with_no_users_in_csv = []
        actual_with_no_users_in_csv = users._get_all_users()

        assert actual_with_no_users_in_csv == expected_with_no_users_in_csv

        users.signup(standard_user)

        expected_with_one_user_in_csv = [
            {
                "id": "1",
                "name": "Naruto Uzumaki",
                "email": "naruto@konoha.com",
                "password": "imgoingtobeahokage123",
                "age": 19,
            }
        ]

        actual_with_one_user_in_csv = users._get_all_users()

        assert actual_with_one_user_in_csv == expected_with_one_user_in_csv

    def test_get_user(self, users_model, standard_user):
        users, filename = users_model

        users.signup(standard_user)

        expected_when_user_not_found = {}
        actual_when_user_not_found = users.get_user(20)

        assert actual_when_user_not_found == expected_when_user_not_found

        expected_when_user_found = {
            "id": "1",
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "age": 19,
            "password": "imgoingtobeahokage123",
        }

        actual_when_user_found = users.get_user(1)

        assert actual_when_user_found == expected_when_user_found
