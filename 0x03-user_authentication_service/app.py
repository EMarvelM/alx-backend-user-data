#!/usr/bin/env python3
""" Module for basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
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
            result = jsonify({"email": email, "message": "logged in"})
            res = make_response(result)
            if session_id:
                res.set_cookie("session_id", session_id)
                return res
        else:
            return abort(401)
    else:
        return abort(400)


@app.route("/logout", strict_slashes=False, methods=["DELETE"])
def logout():
    """ Route to destroy the session of the user and redirect to the home page

    Returns:
        redirect: to the home page
    """
    session_id = request.cookies.get("session_id", None)
    
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            return abort(403)
    else:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
