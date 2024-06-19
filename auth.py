#!/usr/bin/python3
"""Module for handling user authentication.

This module provides functions for registering new users,
logging in users, and managing user passwords. It ensures
secure authentication and adheres to data privacy standards.
"""

import re
import bcrypt
import jwt
from database import get_user_by_username, create_user, update_user_password

SECRET_KEY = "your_secret_key"  # Use a secure key and keep it secret


def validate_password(password):
    """Validate the password to meet security criteria."""
    if len(password) < 6:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def register_user(username, password, **kwargs):
    """Register a new user with the provided credentials.

    Parameters:
    - username (str): The username for the new user.
    - password (str): The password for the new user.
    - **kwargs: Additional user information (e.g., full name, date of birth).

    Returns:
    - bool: True if registration is successful, False otherwise.
    """
    if get_user_by_username(username):
        return False

    if not validate_password(password):
        raise ValueError("Password does not meet security criteria")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = create_user(username, hashed_password, **kwargs)

    return bool(user_id)


def login_user(username, password):
    """Log in a user with the provided credentials.

    Parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.

    Returns:
    - dict: User information if login is successful, None otherwise.
    """
    user = get_user_by_username(username)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        token = jwt.encode({"user_id": user['id']}, SECRET_KEY, algorithm='HS256')
        return {"user_id": user['id'], "token": token}

    return None


def reset_password(username, new_password):
    """Reset the user's password.

    Parameters:
    - username (str): The username of the user.
    - new_password (str): The new password for the user.

    Returns:
    - bool: True if password reset is successful, False otherwise.
    """
    if not validate_password(new_password):
        raise ValueError("Password does not meet security criteria")

    user = get_user_by_username(username)
    if user:
        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        update_user_password(user['id'], hashed_new_password)
        return True

    return False
