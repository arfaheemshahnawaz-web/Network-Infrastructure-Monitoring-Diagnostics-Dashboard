import ipaddress
import json
import re
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "0.0.0.0"
PORT = 8765

def get_lan_ip():
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    finally:
        sock.close()
def get_arp_table():
    result = subprocess.run(
        ["arp", "-a"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )

    arp_table = {}

    for line in result.stdout.splitlines():
        match = re.search(
            r"^\s*(\d+\.\d+\.\d+\.\d+)\s+"
            r"([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})",
            line,
        )

        if not match:
            continue

        ip = match.group(1)
        mac = match.group(2).replace("-", ":").lower()

        address = ipaddress.ip_address(ip)

        if address.is_multicast or address.is_unspecified:
            continue

        if ip.endswith(".255"):
            continue

        arp_table[ip] = mac

    return arp_table


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != "/arp":
            self.send_response(404)
            self.end_headers()
            return

        data = get_arp_table()

        response = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def log_message(self, format, *args):
        return




lan_ip = get_lan_ip()

server = HTTPServer((HOST, PORT), Handler)

print(f"Network agent running on port {PORT}...")
print(f"LAN IP: {lan_ip}")

server.serve_forever()