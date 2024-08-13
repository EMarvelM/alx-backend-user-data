#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


from user import Base
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """ DB class
    """

    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add a new user to the database

        Args:
            email (str): email
            hashed_password (str): hashed password

        Returns:
            User: User object
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password

        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, *args, **kwargs) -> User:
        """ Find a user by a given attribute

        Args:
            *args: arguments
            **kwargs: keyword arguments

        Returns:
            User: User object
        """
        try:
            result = self.__session.query(User).filter_by(**kwargs).first()
            if not hasattr(result, "id"):
                raise NoResultFound("NoResultFound")
            return result
        except AttributeError:
            raise InvalidRequestError("InvalidRequestError")
        except KeyError:
            raise InvalidRequestError("InvalidRequestError")

    def update_user(self, user_id, *args, **kwargs) -> None:
        user = self.find_user_by(id=user_id)
        for i, j in kwargs.items():
            if not hasattr(user, i):
                raise ValueError
            else:
                setattr(user, i, j)
        self._session.commit()
