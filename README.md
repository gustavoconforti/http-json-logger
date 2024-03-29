# HTTP JSON Logger

This project provides a simple HTTP endpoint that allows you to receive HTTP POST requests with JSON payloads, store the data in a log file and send it to a syslog capable server. Useful for integration with log analysis tools that do not offer this feature but are able to consume local log files or receive syslog messages.

> [!NOTE]  
> Starting from version 4.6, the `/events` endpoint is available in the Wazuh API - the tool that initially demanded this script - enabling the event ingestion directly through HTTP requests.
> The file [`send-to-wazuh-api.py`](send-to-wazuh-api.py) exemplifies how to do so.

## Prerequisites

Before you can run the project, you'll need to install the necessary dependencies using `pip3`:

```bash
pip3 install gunicorn flask flask-talisman
```

It is also advisable to create a log file directory and set the appropriate permissions.

```bash
sudo mkdir /path/to/log
```

The script has the path hardcoded to `/var/log/http-json-logger/requests.log`, change according to your needs.

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
ExecStart=/usr/local/bin/gunicorn --workers 2 -b 0.0.0.0:55001 --certfile /path/to//public.crt --keyfile /path/to//private.key http_json_logger:app
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

<p align="center">
  <img src="https://github.com/gustavoconforti/wazuh-honeypot/assets/56703129/d30da931-de3a-44dd-93d5-cfa2c63f6331" style="width:50%;">
</p>

## License
This project is licensed under the [GNU General Public License, Version 3 (GPL-3.0)](LICENSE). See the [LICENSE](LICENSE) file for details.
