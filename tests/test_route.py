from flask import Flask
from pytest import fixture
from os import remove

from app import create_app


@fixture
def app():
    return create_app()


@fixture
def client(app: Flask):
    yield app.test_client()

    remove("data/users_test.csv")


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
            "age": "19",
        }

        expected_status = 201

        response = client.post("/signup", json=given)

        actual_body = response.get_json()
        actual_status = response.status_code

        assert actual_body == expected_body
        assert actual_status == expected_status

    def test_signup_duplicated(self, client):
        given = {
            "name": "Naruto Santos",
            "email": "naruto@konoha.com",
            "password": "eunaosouoNaruto123",
            "age": 20,
        }

        expected_body = {}
        expected_status = 422

        response = client.post("/signup", json=given)
        actual_body = response.get_json()
        actual_status = response.status

        assert actual_body == expected_body
        assert actual_status == expected_status
