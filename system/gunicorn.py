import json

host = "0.0.0.0"
port = "8001"

workers_per_core = 1

# Gunicorn config variables
loglevel = "error"
workers = 2
bind = f"{host}:{port}"
keepalive = 120
errorlog = "-"
max_requests = 10000
max_requests_jitter = 10000
timeout = 10
backlog = 2048
capture_output = True

log_data = {
    "host": host,
    "port": port,
    "loglevel": loglevel,
    "bind": bind,
}
print(json.dumps(log_data))
