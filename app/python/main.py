from flask import Flask, request
import requests
import schedule
import time
import threading
from ipaddress import ip_address, ip_network

app = Flask(__name__)

ALLOWED_IP_RANGES = []

def get_allowed_ips(allowed_ip_ranges):
    AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    AWS_REGION = "eu-west-1"
    try:
        # Get IP ranges from AWS
        response = requests.get(AWS_IP_RANGES_URL)
        response.raise_for_status()
        data = response.json()

        # Filter IP ranges for the specific AWS region
        allowed_ip_ranges = [
            prefix["ip_prefix"] for prefix in data["prefixes"] if prefix["region"] == AWS_REGION
        ]
        print("Allowed IP ranges updated:", allowed_ip_ranges)
    except Exception as e:
        print("Failed to update allowed IP ranges:", e)

def is_ip_allowed(client_ip, allowed_ip_ranges):
    for ip_range in allowed_ip_ranges:
        if ip_address(client_ip) in ip_network(ip_range):
            return True
    return False

def run_scheduler():
    """Runs the schedule in a separate thread."""
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/", methods=["POST"])
def check_access():
    client_ip = request.remote_addr

    if is_ip_allowed(client_ip, ALLOWED_IP_RANGES):
        return "OK", 200
    else:
        return "Unauthorized", 401

if __name__ == "__main__":
    get_allowed_ips(ALLOWED_IP_RANGES)

    schedule.every(1).day.do(get_allowed_ips, ALLOWED_IP_RANGES)
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    app.run(host="0.0.0.0", port=5000)