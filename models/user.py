import uuid
from typing import Dict
from werkzeug.security import check_password_hash

from common.database import Database


class User:

    collection = "users"

    def __init__(self, username, pwd_hash, _id=None):
        self.username = username
        self.pwd_hash = pwd_hash
        self._id = _id or uuid.uuid4().hex

    def json(self):
        return {"_id": self._id, "username": self.username, "pwd_hash": self.pwd_hash}

    def login_valid(self, password):
        """
        Check if credentials inserted makes a valid loggin,
        if so, this function will return a boolean True value, and a string,
        else will return a boolean False value and a string.

        :username arg: Username as a str.
        :password arg: Password as a str.
        :bool return: True or False, indicating if we can log in or not.
        :str return: A text message explaining why it succedded of failed.
        """

        # Ensure username was submitted
        if not self.username:
            return False, "must provide username"

        # Ensure password was submitted
        elif not password:
            return False, "must provide password"

        else:
            row = Database.find_one(User.collection, {"username": self.username})

            # Make sure there is a user
            if not row:
                return False, "Username not found."

            elif check_password_hash(row.get("pwd_hash"), password):
                return True, f"Logged In as {self.username} successfully!"
            else:
                return False, "Password Invalid."

    def register_valid(self, confirmation):
        """
        Check if credentials inserted are valid, if so,
        then check the username is unique. If it is unique,
        return a bool and a string message.

        :username arg: Username as a str.
        :password arg: Password as a str.
        :confirmation arg: String confirmation used to compare with password.
        :bool return: True or False, indicating if we can log in or not.
        :str return: A text message explaining why it succedded of failed.
        """

        # Ensure username was submitted
        if not self.username:
            return False, "must provide username"

        # Ensure password was submitted
        elif not self.pwd_hash:
            return False, "must provide password"

        # Ensure confirmation was submitted
        elif not confirmation:
            return False, "must provide password confirmation"

        # Ensure password and confirmation match
        elif not check_password_hash(self.pwd_hash, confirmation):
            return False, "password and confirmation must match"

        else:
            row = Database.find_one("users", {"username": self.username})

            # Ensure username is unique
            if row:
                return False, "This username is already taken."

            else:
                return True, f"Registered successfully as {self.username} !"

    def insert_to_db(self) -> None:
        """
        Insert the current usert into db.

        :return: None
        """
        Database.insert(collection=User.collection, data=self.json())

    @classmethod
    def get_user(cls, username) -> Dict:
        """
        Find the username in the database, and return None if no user with
        the username key was found, else return a dictionary with
        the user data.
        """
        user = Database.find_one(cls.collection, {"username": username})
        return {"_id": user["_id"], "username": user["username"]}
