#!/usr/bin/env python3

from flask import Flask, request, jsonify
import json
import os
import logging
from flask_talisman import Talisman

app = Flask(__name__)

# Configure the logging settings
log_file = '/var/log/http-json-logger/requests.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define the expected fields
expected_fields = ["request_method", "host", "status"]

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
            return jsonify({"error": "Authentication failed"}), 401  # Unauthorized

        # Check if the request contains JSON data
        if request.is_json:
            data = request.get_json()

            # Perform data validation
            if validate_data(data):
                # Log the JSON data to the file
                with open(log_file, 'a') as log:
                    log.write(json.dumps(data) + '\n')

                return jsonify({"message": "JSON data logged successfully"}), 200
            else:
                return jsonify({"error": "Invalid JSON data"}), 400
        else:
            return jsonify({"error": "Invalid JSON data"}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON data"}), 400  # Return a generic error for unhandled exceptions

def validate_data(data):
    # Check if data contains only the expected fields
    return set(data.keys()) == set(expected_fields)

if __name__ == '__main__':
    # Ensure the log file exists
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            log.write("Logs:\n")

    app.run(host='0.0.0.0', port=55001)
