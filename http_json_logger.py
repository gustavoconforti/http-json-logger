#!/usr/bin/env python3

from flask import Flask, request, jsonify
import json
import os
import logging
import socket
from flask_talisman import Talisman

app = Flask(__name__)

# Configure the logging settings
log_file = '/var/log/http-json-logger/requests.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Configure the syslog server
udp_ip = '192.168.0.1'
udp_port = 514

# Define the expected fields
expected_fields = ["data_source", "original_timestamp", "event"]


# Configure Talisman with security headers
csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\'',
    'style-src': '\'self\'',
    'img-src': '*',
    'font-src': '\'self\'',
    'object-src': '\'none\'',
    'frame-src': '\'none\'',
    'base-uri': '\'self\'',
    'frame-ancestors': '\'none\'',
    'form-action': '\'self\'',
}

talisman = Talisman(
    app,
    content_security_policy=csp,
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True,
    session_cookie_http_only=True,
    referrer_policy='strict-origin-when-cross-origin',
)

@app.route('/log', methods=['POST'])
def log_json():
    try:
        # Check for the custom authentication header and value
        auth_header = request.headers.get('X-Auth-Token')
        if auth_header is None or auth_header != 'test_token':
            return jsonify({"error": "Authentication failed"}), 401

        # Check if the request contains JSON data
        if request.is_json:
            data = request.get_json()

            # Perform data validation
            if validate_data(data):
                # Log the JSON data to the file
                with open(log_file, 'a') as log:
                    log.write(json.dumps(data) + '\n')

                # Send JSON data to the UDP server
                send_to_udp_server(data)

                return jsonify({"message": "Success"}), 200
            else:
                return jsonify({"error": "Error"}), 400
        else:
            return jsonify({"error": "Error"}), 400
    except Exception as e:
        return jsonify({"error": "Error"}), 400

def validate_data(data):
    # Check if data contains only the expected fields
    return set(data.keys()) == set(expected_fields)

def send_to_udp_server(data):
    try:
        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send the JSON data to the UDP server
        udp_socket.sendto(json.dumps(data).encode(), (udp_ip, udp_port))

        # Close the socket
        udp_socket.close()
    except Exception as e:
        print("Error sending data to UDP server:", str(e))

if __name__ == '__main__':
    # Ensure the log file exists
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            log.write("Logs:\n")

    app.run(host='0.0.0.0', port=55001)
