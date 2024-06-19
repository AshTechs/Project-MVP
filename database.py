#!/usr/bin/python3
"""Module for managing database connections.

This module handles the creation and management of database
connections, queries, and data manipulation for the app.
"""

import mysql.connector
from mysql.connector import Error

def connect_to_database():
    """Connect to the MySQL database.

    Returns:
    - connection: A connection object to the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your_database_name',
            user='your_username',
            password='your_password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
    return None

def close_connection(connection):
    """Close the database connection.

    Parameters:
    - connection: The database connection to close.

    Returns:
    - None
    """
    if connection.is_connected():
        connection.close()

def get_user_by_username(username):
    """Retrieve a user by their username.

    Parameters:
    - username (str): The username of the user.

    Returns:
    - dict: The user's details if found, None otherwise.
    """
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        close_connection(connection)
        return user
    return None

def create_user(username, hashed_password, **kwargs):
    """Create a new user in the database.

    Parameters:
    - username (str): The username of the new user.
    - hashed_password (str): The hashed password of the new user.
    - **kwargs: Additional user information.

    Returns:
    - int: The ID of the newly created user.
    """
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, full_name, date_of_birth, gender, location, phone_number) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (username, hashed_password, kwargs.get('full_name'), kwargs.get('date_of_birth'), kwargs.get('gender'), kwargs.get('location'), kwargs.get('phone_number'))
        )
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        close_connection(connection)
        return user_id
    return None

def update_user_password(user_id, hashed_password):
    """Update a user's password in the database.

    Parameters:
    - user_id (int): The ID of the user.
    - hashed_password (str): The new hashed password.

    Returns:
    - None
    """
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))
        connection.commit()
        cursor.close()
        close_connection(connection)

def create_appointment(user_id, doctor_id, services, appointment_datetime, description):
    """Create a new appointment in the database.

    Parameters:
    - user_id (int): The ID of the user (patient).
    - doctor_id (int): The ID of the doctor.
    - services (list): A list of services to be booked.
    - appointment_datetime (datetime): The appointment date and time.
    - description (str): A brief description of the medical condition.

    Returns:
    - int: The ID of the newly created appointment.
    """
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO appointments (user_id, doctor_id, services, appointment_datetime, description) VALUES (%s, %s, %s, %s, %s)",
            (user_id, doctor_id, ','.join(services), appointment_datetime, description)
        )
        connection.commit()
        appointment_id = cursor.lastrowid
        cursor.close()
        close_connection(connection)
        return appointment_id
    return None

def cancel_appointment_by_id(appointment_id):
    """Cancel an appointment in the database.

    Parameters:
    - appointment_id (int): The ID of the appointment to cancel.

    Returns:
    - bool: True if cancellation is successful, False otherwise.
    """
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
        connection.commit()
        cursor.close()
        close_connection(connection)
        return True
    return False

def get_appointments_by_user(user_id, role):
    """Retrieve appointments for a user.

    Parameters:
    - user_id (int): The ID of the user (patient or doctor).
    - role (str): The role of the user ('patient' or 'doctor').

    Returns:
    - list: A list of appointments.
    """
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor(dictionary=True)
        if role == 'patient':
            cursor.execute("SELECT * FROM appointments WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("SELECT * FROM appointments WHERE doctor_id = %s", (user_id,))
        appointments = cursor.fetchall()
        cursor.close()
        close_connection(connection)
        return appointments
    return None
