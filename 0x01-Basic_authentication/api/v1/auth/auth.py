from flask import request
from typing import List, TypeVar


class Auth():
    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        return False

    def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
