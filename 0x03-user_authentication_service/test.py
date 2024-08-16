#!/usr/bin/env python3
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    """Test the home route."""
    response = requests.get(f"{BASE_URL}/")
    print("Home Test:", response.json())

def test_user_registration():
    """Test the user registration route."""
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users", data=data)
    print("User Registration Test:", response.json())

def test_user_registration_existing_email():
    """Test registration with an already registered email."""
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users", data=data)
    print("Existing Email Registration Test:", response.json())

def test_login():
    """Test the login route."""
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    print("Login Test:", response.json())
    return response.cookies.get("session_id")

def test_logout(session_id):
    """Test the logout route."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/logout", cookies=cookies)
    print("Logout Test:", "Successful" if response.status_code == 200 else "Failed", response.status_code)

if __name__ == "__main__":
    test_home()
    test_user_registration()
    test_user_registration_existing_email()
    session_id = test_login()
    if session_id:
        test_logout(session_id)
