import ipaddress
import os
import platform
import socket
import subprocess
import urllib.request
import json
from monitoring.models import Device
from concurrent.futures import ThreadPoolExecutor, as_completed


class DeviceDiscovery:

    @staticmethod
    def get_network():
        network = os.getenv("DISCOVERY_NETWORK")

        if not network:
            raise ValueError("DISCOVERY_NETWORK is not configured")

        return ipaddress.ip_network(network, strict=False)

    @staticmethod
    def get_mac_addresses():
        """Get MAC addresses from the host network agent."""

        try:
            agent_host = os.getenv(
                "DISCOVERY_AGENT_HOST",
                "host.docker.internal",
            )

            agent_port = int(
                os.getenv("DISCOVERY_AGENT_PORT", "8765")
            )

            host_ip = socket.getaddrinfo(
                agent_host,
                agent_port,
                socket.AF_INET,
                socket.SOCK_STREAM,
            )[0][4][0]

            url = f"http://{host_ip}:{agent_port}/arp"

            with urllib.request.urlopen(url, timeout=3) as response:
                return json.loads(
                    response.read().decode("utf-8")
                )

        except Exception as e:
            print(f"MAC address lookup failed: {e}")
            return {}

    @staticmethod
    def ping(ip):
        system = platform.system()

        if system == "Windows":
            command = [
                "ping",
                "-n",
                "1",
                "-w",
                "1000",
                str(ip),
            ]
        else:
            command = [
                "ping",
                "-c",
                "1",
                "-W",
                "1",
                str(ip),
            ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=3,
            )

            return result.returncode == 0

        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    @staticmethod
    def resolve_hostname(ip):
        try:
            return socket.gethostbyaddr(str(ip))[0]
        except Exception:
            return "Unknown"

    @classmethod
    def scan_host(cls, ip, mac_addresses):
        if not cls.ping(ip):
            return None

        ip_string = str(ip)

        hostname = cls.resolve_hostname(ip_string)

        if hostname == "Unknown":
            hostname = ip_string

        mac_address = mac_addresses.get(ip_string, "Unknown")

        return {
            "ip": ip_string,
            "hostname": hostname,
            "mac": mac_address,
            "status": "Online",
        }

    @classmethod
    def discover(cls):
        network = cls.get_network()

        mac_addresses = cls.get_mac_addresses()

        devices = []

        with ThreadPoolExecutor(max_workers=100) as executor:

            futures = {
                executor.submit(
                    cls.scan_host,
                    ip,
                    mac_addresses,
                ): ip
                for ip in network.hosts()
            }

            for future in as_completed(futures):

                device = future.result()

                if device:
                    devices.append(device)

        devices = sorted(
        devices,
        key=lambda x: ipaddress.ip_address(x["ip"])
        )

        DeviceDiscovery.save_devices(devices)

        return devices
    @staticmethod
    def save_devices(devices):
        """Save discovered devices to the database."""

        saved_devices = []

        for data in devices:
            device, created = Device.objects.update_or_create(
                ip_address=data["ip"],
                defaults={
                    "hostname": data["hostname"],
                    "mac_address": data["mac"],
                    "status": "online",
                    "device_type": "workstation",
                    "os_type": "",
                    "location": "",
                },
            )

            saved_devices.append(device)

        return saved_devices