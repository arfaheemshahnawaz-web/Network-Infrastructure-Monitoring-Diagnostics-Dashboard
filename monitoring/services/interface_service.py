import platform
import subprocess
import psutil
import re

class InterfaceService:
    @staticmethod
    def get_interfaces():
        interfaces =[]
        for interface in psutil.net_if_addrs().keys():
            interfaces.append({
                "name":interface
            })
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
            match= re.search(r"Default Gateway[ .:]*([\d\.]+)",output)

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