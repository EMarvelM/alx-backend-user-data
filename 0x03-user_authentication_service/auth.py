#!/usr/bin/env python3
""" Auth module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ Hash a password
    """
    salt = gensalt(rounds=15)
    return hashpw(password=password.encode("utf-8"), salt=salt)
