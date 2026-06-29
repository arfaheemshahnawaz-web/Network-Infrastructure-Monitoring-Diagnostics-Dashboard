import platform
import subprocess
import psutil
import re
import socket

class InterfaceService:
    @staticmethod
    def get_interfaces():
        interfaces = []
        for name, addresses in psutil.net_if_addrs().items():
            interface = {
                "name": name,
                "ipv4": "",
                "ipv6": "",
                "mac": ""
            }

            for address in addresses:
                if address.family == socket.AF_INET:
                    interface["ipv4"] = address.address

                elif address.family == socket.AF_INET6:
                    interface["ipv6"] = address.address

                elif getattr(psutil, "AF_LINK", None) == address.family:
                    interface["mac"] = address.address

            interfaces.append(interface)

        return interfaces
    

    @staticmethod
    def get_default_gateway():
        if platform.system() == 'Windows':
            result = subprocess.run(
                ['ipconfig'],
                capture_output=True,
                text=True
            )
            output = result.stdout
            match = re.search(r"Default Gateway[^\n]*:\s*([\d\.]+)",output)

            if match:
                return match.group(1)
            
        else:
            result=subprocess.run(
                ["ip","route"],
                capture_output=True,
                text=True
            )
            output=result.stdout.splitlines()
            for line in output:
                if line.startswith("default"):
                    return line.split()[2]
                
        return "Unavailable"
    
    @staticmethod
    def get_dns_servers():
        servers = []

        if platform.system() == "Windows":

            result = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True
            )
            output = result.stdout
            for line in output.splitlines():
                if "DNS Servers" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        servers.append(parts[1].strip())
        else:
            with open("/etc/resolv.conf") as file:
                for line in file:
                    if line.startswith("nameserver"):
                        servers.append(line.split()[1])
        return servers