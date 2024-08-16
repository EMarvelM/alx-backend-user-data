#!/usr/bin/env python3
""" Module for basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def home():
    """ Route for the home page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", strict_slashes=False, methods=["POST"])
def users():
    """ Route to register a user
    """
    data = request.form
    email = data.get("email")
    password = data.get("password")
    if email and password:
        try:
            AUTH.register_user(email, password)
            return jsonify({"email": email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", strict_slashes=False, methods=["POST"])
def login():
    """ Route create a new session for the user, store it the session ID as a
    cookie with key "session_id" on the response and return a JSON payload of
    the form.
    """
    data = request.form
    email = data.get("email")
    password = data.get("password")
    if email and password:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            res = make_response(jsonify({"email": email, "message": "logged in"}))
            if session_id:
                res.set_cookie("session_id", session_id)
        else:
            return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
