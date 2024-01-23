#!/usr/bin/env python3

# --------------------
#  Starting with Wazuh 4.6 the API endpoint /events is available.
#  The following code exemplifies how to interact with it.
# --------------------

import json
import requests
import urllib3
from base64 import b64encode
import time

# Disable insecure https warnings (for self-signed SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_to_wazuh_api(data):
    try:
        # Configuration
        protocol = 'https'
        host = 'localhost'
        port = 55000
        user = 'user'
        password = 'password'
        login_endpoint = 'security/user/authenticate'

        login_url = f"{protocol}://{host}:{port}/{login_endpoint}"
        basic_auth = f"{user}:{password}".encode()
        login_headers = {'Content-Type': 'application/json',
                         'Authorization': f'Basic {b64encode(basic_auth).decode()}'}

        # Login request
        response = requests.post(login_url, headers=login_headers, verify=False)
        token = json.loads(response.content.decode())['data']['token']

        # New authorization header with the JWT token we got
        requests_headers = {'Content-Type': 'application/json',
                            'Authorization': f'Bearer {token}'}

        # Body as JSON payload
        escaped_data = json.dumps(data)
        body = {
            "events": [
                escaped_data
                ]
            }

        # Send event
        response = requests.post(
            f"{protocol}://{host}:{port}/events",
            headers=requests_headers,
            json=body,
            verify=False
        )
        
        return response.text
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    send_to_wazuh_api()
