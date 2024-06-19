#!/usr/bin/python3
"""Module for defining API routes.

This module maps API endpoints to appropriate functions in
the app's modules, allowing for efficient handling of requests.
"""

from flask import Flask, request, jsonify
from auth import register_user, login_user, reset_password
from appointment import book_appointment, cancel_appointment, get_appointments

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    """API endpoint for user registration."""
    data = request.json
    try:
        username = data['username']
        password = data['password']
        full_name = data.get('full_name')
        date_of_birth = data.get('date_of_birth')
        gender = data.get('gender')
        location = data.get('location')
        phone_number = data.get('phone_number')
        if register_user(
                username, password,
                full_name=full_name,
                date_of_birth=date_of_birth,
                gender=gender,
                location=location,
                phone_number=phone_number):
            return jsonify({"message": "User registered successfully"}), 201
        return jsonify({"message": "Username already exists"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    """API endpoint for user login."""
    data = request.json
    try:
        username = data['username']
        password = data['password']
        user = login_user(username, password)
        if user:
            return jsonify(user), 200
        return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/reset_password', methods=['POST'])
def reset_password_route():
    """API endpoint for password reset."""
    data = request.json
    try:
        username = data['username']
        new_password = data['new_password']
        if reset_password(username, new_password):
            return jsonify({"message": "Password reset successfully"}), 200
        return jsonify({"message": "User not found or invalid password"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/book_appointment', methods=['POST'])
def book_appointment_route():
    """API endpoint for booking an appointment."""
    data = request.json
    try:
        user_id = data['user_id']
        doctor_id = data['doctor_id']
        services = data['services']
        date = data['date']
        time = data['time']
        description = data.get('description')
        appointment = book_appointment(user_id, doctor_id, services, date, time, description)
        if appointment:
            return jsonify(appointment), 201
        return jsonify({"message": "Failed to book appointment"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment_route():
    """API endpoint for cancelling an appointment."""
    data = request.json
    try:
        appointment_id = data['appointment_id']
        if cancel_appointment(appointment_id):
            return jsonify({"message": "Appointment cancelled successfully"}), 200
        return jsonify({"message": "Failed to cancel appointment"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/get_appointments', methods=['GET'])
def get_appointments_route():
    """API endpoint for retrieving appointments."""
    try:
        user_id = request.args.get('user_id')
        role = request.args.get('role', 'patient')
        appointments = get_appointments(user_id, role)
        if appointments:
            return jsonify(appointments), 200
        return jsonify({"message": "No appointments found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
