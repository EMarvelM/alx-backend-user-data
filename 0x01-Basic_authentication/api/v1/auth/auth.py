#!/usr/binv/env python3
from flask import request
from typing import List, TypeVar


class Auth():
    def __init__(self) -> None:
        """ Constructor method
        """
        pass

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """ Method that returns True if the path is not in the list of strings

        Args:
            path (str): The path to evaluate
            exclude_paths (List[str]): The list of strings

        Returns:
            bool: True if the path is not in the list of strings
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that returns the value of the Authorization header
        in the request

        Args:
            request ([type], optional): The request. Defaults to None.

        Returns:
            str: The value of the Authorization header in the request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns None

        Args:
            request ([type], optional): The request. Defaults to None.

        Returns:
            TypeVar('User'): None
        """
        return None
