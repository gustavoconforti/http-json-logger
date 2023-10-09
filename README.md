# HTTP JSON Logger

This project provides a simple HTTP endpoint that allows you to log JSON data to a file on your server. It's designed to receive HTTP POST requests with JSON payloads and store the data in a log file. Useful for log analysis tools that do not offer this feature and rely only on local files consumption.

## Prerequisites

Before you can run the project, you'll need to install the necessary dependencies using `pip3`:

```bash
pip3 install gunicorn flask flask-talisman
```

## Running the script
To run the script once, you can use the following command:

```bash
/usr/local/bin/gunicorn --workers 2 -b 0.0.0.0:55001 --certfile /path/to/public.crt --keyfile /path/to/private.key http_json_logger:app
```

Make sure to change the command with the actual paths to your SSL/TLS certificate and private key files.

## Running as a service
To run the script as a service, turn it into a systemd service unit. Create a service file, like `/etc/systemd/system/http-json-logger.service`:

```ini
[Unit]
Description=HTTP JSON Logger Service
After=network.target

[Service]
User=your_username
ExecStart=/usr/local/bin/gunicorn --workers 2 -b 0.0.0.0:55001 --certfile /etc/cusco-azul/certs/public.crt --keyfile /etc/cusco-azul/certs/private.key http_json_logger:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Replace `your_username` with the username you want to run the service as.

Enable and start the service:

```bash
sudo systemctl enable http-json-logger.service
sudo systemctl start http-json-logger.service
```

Now, the script will run as a service and automatically start on system boot.

## Testing
You can test the script using `curl` to send HTTP POST requests with JSON payloads. Here are some example `curl` commands:

```bash
# Log a GET request with a 200 status code
curl -k -X POST -H "X-Auth-Token: test_token" -H "Content-Type: application/json" -d '{"request_method": "GET", "host": "www.onedomain.com", "status": "200"}' https://server-ip:55001/log

# Log a POST request with a 403 status code
curl -k -X POST -H "X-Auth-Token: test_token" -H "Content-Type: application/json" -d '{"request_method": "POST", "host": "www.test.com", "status": "403"}' https://server-ip:55001/log

# Log a GET request with a 302 status code
curl -k -X POST -H "X-Auth-Token: test_token" -H "Content-Type: application/json" -d '{"request_method": "GET", "host": "www.contoso.com", "status": "302"}' https://server-ip:55001/log
```

Make sure to replace `test_token`, `server-ip`, and adjust the JSON payloads as needed for your testing scenarios.

## Contribution
Contributions and enhancements to this project are welcome. Please fork the repository, make your improvements, and submit a pull request. Be sure to adhere to the project's coding standards and guidelines.

## License
This project is licensed under the [GNU General Public License, Version 3 (GPL-3.0)](LICENSE). See the [LICENSE](LICENSE) file for details.

## Disclaimer
This repository is for educational and research purposes only. Deploying honeypots on a network without proper authorization may be illegal in some jurisdictions. Use responsibly and in compliance with applicable laws and regulations.
