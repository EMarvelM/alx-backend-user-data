#!/usr/bin/env python3
"""
Main file
"""
import requests
_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """ Register a new user

    Args:
        email (str): email
        password (str): password

    Returns:
        None
    """
    url = _URL + "/users"
    res = requests.post(url, data={"email": email, "password": password})
    assert(res.json() is not None)
    assert(res.json() == {"email": email, "message": "user created"})
    assert(res.status_code == 200)

    res = requests.post(url, data={"email": email, "password": password})
    assert(res.status_code == 400)
    assert(res.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """ Log in with wrong password

    Args:
        email (str): email
        password (str): password

    Return:
        None
    """
    url = _URL + "/sessions"
    res = requests.post(url, data={"email": email, "password": password})
    assert(res.status_code == 401)


def profile_unlogged() -> None:
    """ Get the profile of the user

    Args:
        None

    Returns:
        None
    """
    url = _URL + "/profile"
    res = requests.get(url)
    assert(res.status_code == 403)

    from uuid import uuid4
    cookies = {"session_id": str(uuid4())}
    res = requests.get(url, cookies=cookies)
    assert(res.status_code == 403)


def log_in(email: str, password: str) -> str:
    """ Log in the user

    Args:
        email (str): email
        password (str): password

    Return:
        str: session id
    """
    url = _URL + "/sessions"
    res = requests.post(url, data={"email": email, "password": password})
    assert(res.status_code == 200)
    assert("session_id" in res.cookies)
    return res.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """ Get the profile of the user

    Args:
        session_id (str): session id

    Returns:
        None
    """
    url = _URL + "/profile"
    cookies = {"session_id": session_id}
    res = requests.get(url, cookies=cookies)
    assert(res.status_code == 200)
    assert("email" in res.json())
    assert(res.json().get("email") == EMAIL)


def log_out(session_id: str) -> None:
    """ Log out the user

    Args:
        session_id (str): session id

    Returns:
        None
    """
    url = _URL + "/sessions"
    cookies = {"session_id": session_id}
    res = requests.delete(url, cookies=cookies)
    assert(res.status_code == 200)

    url = _URL + "/profile"
    cookies = {"session_id": session_id}
    res = requests.get(url, cookies=cookies)
    assert(res.status_code == 403)


def reset_password_token(email: str) -> str:
    """ Retrive the password reset token

    Args:
        email (str): email

    Returns:
        str: reset token
    """
    url = _URL + "/reset_password"
    res = requests.post(url, data={"email": email})
    assert(res.ok)
    assert(res.status_code == 200)
    assert("reset_token" in res.json())
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> str:
    """ Update the password

    Args:
        email (str): email
        reset_token (str): reset token
        new_password (str): new password

    Returns:
        None
    """
    url = _URL + "/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    res = requests.put(url, data=data)
    assert(res.ok)
    assert(res.status_code == 200)
    assert("message" in res.json() and "email" in res.json())
    assert(res.json().get("message") == "Password updated")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
