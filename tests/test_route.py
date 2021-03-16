from flask import Flask
from pytest import fixture

from app import create_app


@fixture
def app():
    return create_app()


@fixture
def client(app: Flask):
    return app.test_client()


class TestSignup:
    def test_signup_standard(self, client):
        given = {
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "password": "imgoingtobeahokage123",
            "age": 19,
        }

        expected_response = {
            "id": "1",
            "name": "Naruto Uzumaki",
            "email": "naruto@konoha.com",
            "age": 19,
        }
        actual_response = client.post("/signup", json=given)

        assert actual_response == expected_response

    def test_signup_duplicated(self, client):
        given = {
            "name": "Naruto Santos",
            "email": "naruto@konoha.com",
            "password": "eunaosouoNaruto123",
            "age": 20,
        }

        expected_response = {}
        expected_status = "422 UNPROCESSABLE ENTITY"

        response = client.post("/signup", json=given)
        actual_response = response.get_json()
        actual_status = response.status

        assert actual_response == expected_response
        assert actual_status == expected_status
