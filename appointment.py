#!/usr/bin/python3
"""Module for managing medical appointments.

This module handles booking appointments, scheduling,
and tracking for patients and doctors.
"""

from datetime import datetime
from database import create_appointment, get_appointments_by_user, cancel_appointment_by_id


def book_appointment(user_id, doctor_id, services, date, time, description=None):
    """Book a medical appointment.

    Parameters:
    - user_id (int): The ID of the user (patient).
    - doctor_id (int): The ID of the doctor.
    - services (list): A list of services to be booked.
    - date (str): The appointment date (YYYY-MM-DD).
    - time (str): The appointment time (HH:MM).
    - description (str, optional): Brief description of the medical condition.

    Returns:
    - dict: Appointment details if booking is successful, None otherwise.
    """
    # Convert date and time to a datetime object
    appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

    # Create the appointment in the database
    appointment_id = create_appointment(user_id, doctor_id, services, appointment_datetime, description)

    if appointment_id:
        return {
            "appointment_id": appointment_id,
            "user_id": user_id,
            "doctor_id": doctor_id,
            "services": services,
            "datetime": appointment_datetime,
            "description": description
        }
    return None


def cancel_appointment(appointment_id):
    """Cancel a medical appointment.

    Parameters:
    - appointment_id (int): The ID of the appointment.

    Returns:
    - bool: True if cancellation is successful, False otherwise.
    """
    return cancel_appointment_by_id(appointment_id)


def get_appointments(user_id, role='patient'):
    """Retrieve appointments for a user.

    Parameters:
    - user_id (int): The ID of the user (patient or doctor).
    - role (str): The role of the user ('patient' or 'doctor').

    Returns:
    - list: A list of appointments.
    """
    appointments = get_appointments_by_user(user_id, role)
    return appointments
