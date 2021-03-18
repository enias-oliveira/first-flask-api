from flask import Flask
from pytest import fixture
from os import remove, path

from app import create_app


@fixture
def app():
    return create_app()


@fixture
def client(app: Flask):
    test_path = "data/users_test.csv"

    yield app.test_client()

    if path.isfile(test_path):
        remove(test_path)


class TestSignup:
    def test_signup_standard(self, client):
        given = {
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "password": "imgoingtobeahokage123",
            "age": 19,
        }

        expected_body = {
            "id": "1",
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "age": 19,
        }

        expected_status = 201

        response = client.post("/signup", json=given)

        actual_body = response.get_json()
        actual_status = response.status_code

        assert actual_body == expected_body
        assert actual_status == expected_status

    def test_signup_duplicated(self, client):
        first_signup = {
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "password": "imgoingtobeahokage123",
            "age": 19,
        }

        second_signup = {
            "name": "Naruto Santos",
            "email": "naruto@konoha.com",
            "password": "eunaosouoNaruto123",
            "age": 20,
        }

        expected_body = {}
        expected_status_code = 422

        client.post("/signup", json=first_signup)
        response = client.post("/signup", json=second_signup)

        actual_body = response.get_json()
        actual_status_code = response.status_code

        assert actual_body == expected_body
        assert actual_status_code == expected_status_code


class TestLogin:
    def test_login_standard(self, client):
        given = {"email": "naruto@konoha.com", "password": "imgoingtobeahokage123"}
        standard_user = {
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "password": "imgoingtobeahokage123",
            "age": 19,
        }

        client.post("/signup", json=standard_user)

        expected_response_body = {
            "id": "1",
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "age": 19,
        }

        expected_response_status = 200

        response = client.post("/login", json=given)

        actual_body = response.get_json()
        actual_status = response.status_code

        assert actual_body == expected_response_body
        assert actual_status == expected_response_status

    def test_login_invalid_credentials(self, client):
        given = {"email": "saske@konoha.com", "password": "imgoingtobeahokage123"}

        expected_response_body = {}

        expected_response_status = 401

        response = client.post("/login", json=given)

        actual_body = response.get_json()
        actual_status = response.status_code

        assert actual_body == expected_response_body
        assert actual_status == expected_response_status


class TestProfile:
    def test_profile_patch_standard(self, client):
        standard_user = {
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "password": "imgoingtobeahokage123",
            "age": 19,
        }
        client.post("/signup", json=standard_user)

        given = {"age": 21}
        response = client.patch("/profile/1", json=given)

        expected_response_status = 200
        expected_response_body = {
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "password": "imgoingtobeahokage123",
            "age": 21,
        }

        actual_body = response.get_json()
        actual_status = response.status_code

        assert actual_body == expected_response_body
        assert actual_status == expected_response_status

    def test_delete_standard(self, client):
        standard_user = {
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "password": "imgoingtobeahokage123",
            "age": 19,
        }
        client.post("/signup", json=standard_user)

        expected_response_body = ""
        expected_response_status = 204

        response = client.delete("/profile/1")

        actual_body = response.get_json()
        actual_status = response.status_code

        assert actual_body == expected_response_body
        assert actual_status == expected_response_status
