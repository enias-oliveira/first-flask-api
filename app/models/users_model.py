#!/usr/bin/env python3

import csv
import os


class UsersModel:
    def __init__(self, filename) -> None:
        self.filename = filename

    def signup(self, user: dict):
        file_headers = ["id", "name", "age", "email", "password"]

        if self._is_email_registered(user["email"]):
            return {}

        with open(self.filename, "a+") as writable_file:
            writer = csv.DictWriter(writable_file, fieldnames=file_headers)

            if not os.stat(self.filename).st_size:
                writer.writeheader()

            new_user_id = self._get_new_id()
            user_with_id = {"id": new_user_id, **user}

            writer.writerow(user_with_id)

        return self.get_user(new_user_id)

    def _get_new_id(self):
        with open(self.filename, "r") as readable:
            reader = csv.DictReader(readable)
            id_list = [user["id"] for user in list(reader)]

            if not id_list:
                return 1
            else:
                last_id = int(max(id_list))
                return last_id + 1

    def _get_all_users(self):
        try:
            with open(self.filename, "r") as readable:
                reader = csv.DictReader(readable)
                return list(reader)
        except FileNotFoundError:
            return []

    def get_user(self, id):
        users = self._get_all_users()

        try:
            searched_user = next(user for user in users if user["id"] == str(id))
            return {
                key: searched_user[key]
                for key in searched_user.keys() & {"id", "name", "email", "age"}
            }
        except StopIteration:
            return {}

    def _is_email_registered(self, email):
        users = self._get_all_users()

        emails = [user["email"] for user in users]
        return email in emails