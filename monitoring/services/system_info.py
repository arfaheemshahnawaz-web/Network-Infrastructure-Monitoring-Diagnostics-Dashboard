import socket
import platform
import psutil

class SystemInfoService:
    @staticmethod
    def get_info():
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
        except Exception:
            ip_address="Unavailable"
        
        return{
            "hostname": hostname,
            "os": platform.platform(),
            "machine":platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "ip_address": ip_address,
        }