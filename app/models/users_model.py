#!/usr/bin/env python3

import csv
import os


class UsersModel:
    def __init__(self, filename) -> None:
        self.filename = filename

    def signup(self, user: dict):
        file_headers = ["id", "name", "age", "email", "password"]

        with open(self.filename, "a+") as writable_file:
            writer = csv.DictWriter(writable_file, fieldnames=file_headers)

            if not os.stat(self.filename).st_size:
                writer.writeheader()

            new_user_id = self._get_new_id()
            user_with_id = {"id": new_user_id, **user}

            writer.writerow(user_with_id)

        written_user = self.get_user(new_user_id)

        return {
            key: written_user[key]
            for key in written_user.keys() & {"id", "name", "email", "age"}
        }

    def _get_new_id(self):
        with open(self.filename, "r") as readable:
            reader = csv.DictReader(readable)
            users_list = list(reader)

            if not users_list:
                return 1
            else:
                last_id = int(users_list[-1]["id"])
                return last_id + 1

    def get_user(self, id):
        with open(self.filename, "r") as readable:
            reader = csv.DictReader(readable)
            users_list = list(reader)

            return next(user for user in users_list if user["id"] == str(id))
