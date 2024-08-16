#!/usr/bin/env python3
""" Auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from typing import Union


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

    def create_session(self, email: str) -> str:
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=user.session_id)
            return user.session_id
        except NoResultFound:
            pass
        except InvalidRequestError:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrive a user from a session id

        Args:
            session_id (str): session id to get a user

        Returns:
            the corresponding User or None
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ updates the corresponding user’s session ID to None

        Args:
            user_id (int): the user primnary key

        Return:
            None
        """
        self._db.update_user(user_id, session_id=None)


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
