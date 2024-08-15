#!/usr/bin/env python3
""" Auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


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
            if email and password:
                hashed_password = _hash_password(password)
                return self._db.add_user(email, hashed_password)
        except InvalidRequestError:
            if email and password:
                hashed_password = _hash_password(password)
                return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        try:
            user = self._db.find_user_by(email=email)
            if checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False
        except InvalidRequestError:
            return False


def _generate_uuid() -> str:
    """ string representation of new uuid

    Return:
        (str): new uuid
    """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """ Hash a password
    """
    salt = gensalt(rounds=15)
    return hashpw(password=password.encode("utf-8"), salt=salt)
