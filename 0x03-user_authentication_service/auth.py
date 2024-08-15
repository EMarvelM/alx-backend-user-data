#!/usr/bin/env python3
""" Auth module
"""
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user

        Args:
            email (str): email
            password (str): password

        Returns:
            User: User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=hashed_password)


def _hash_password(password: str) -> bytes:
    """ Hash a password
    """
    salt = gensalt(rounds=15)
    return hashpw(password=password.encode("utf-8"), salt=salt)
