#!/usr/bin/env python3

import csv
import os


class UsersModel:
    def __init__(self, filename) -> None:
        self.filename = filename

    def signup(self, user: dict):
        file_headers = ["id", "name", "age", "email", "password"]

        user["email"] = user["email"].lower()

        if self._is_email_registered(user["email"]):
            return {}

        with open(self.filename, "a+") as writable_file:
            writer = csv.DictWriter(writable_file, fieldnames=file_headers)

            if not os.stat(self.filename).st_size:
                writer.writeheader()

            new_user_id = self._get_new_id()
            user_with_id = {"id": str(new_user_id), **user}

            writer.writerow(user_with_id)

            expected_keys = ["id", "name", "email", "age"]
            return {key: user_with_id[key] for key in expected_keys}

    def login(self, credentials):
        users = self._get_all_users()

        try:
            potential_user = next(
                user for user in users if user["email"] == credentials["email"].lower()
            )
            if credentials["password"] == potential_user["password"]:
                expected_keys = ["id", "name", "email", "age"]
                return {key: potential_user[key] for key in expected_keys}

        except StopIteration:
            return {}

    def _get_new_id(self):
        try:
            with open(self.filename, "r") as readable:
                reader = csv.DictReader(readable)
                id_list = [user["id"] for user in list(reader)]

            if not id_list:
                return 1
            else:
                last_id = int(max(id_list))
                return last_id + 1

        except FileNotFoundError:
            return 1

    def _get_all_users(self):
        def convert_age_to_int(user):
            user["age"] = int(user["age"])
            return user

        try:
            with open(self.filename, "r") as readable:
                reader = csv.DictReader(readable)
                return [convert_age_to_int(user) for user in reader]
        except FileNotFoundError:
            return []

    def get_user(self, id):
        users = self._get_all_users()

        try:
            return next(user for user in users if user["id"] == str(id))

        except StopIteration:
            return {}

    def _is_email_registered(self, email):
        users = self._get_all_users()
        emails = [user["email"] for user in users]
        return email in emails

    def update_user(self, id, **kwargs):
        target_user = self.get_user(id)
        target_user.update(kwargs)

        users = self._get_all_users()

        updated_users = [
            user if user["id"] != str(id) else target_user for user in users
        ]

        with open(self.filename, "w") as writable_file:
            file_headers = ["id", "name", "age", "email", "password"]

            writer = csv.DictWriter(writable_file, fieldnames=file_headers)

            writer.writeheader()
            writer.writerows(updated_users)

        expected_keys = ["name", "email", "password", "age"]
        return {key: target_user[key] for key in expected_keys}
