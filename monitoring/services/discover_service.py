import ipaddress
import platform
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

class DeviceDiscovery:
    @staticmethod
    def get_local_ip():
        """Get the local IP address of the machine."""
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('8.8.8.8', 80))
            ip=s.getsockname()[0]

        finally:
            s.close()
        return ip

    @staticmethod
    def ping(ip):
        """Ping a given IP address to check if it's online."""
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', '-w' if platform.system() == 'Windows' else
                   '-W', '1000' if platform.system() == 'Windows' else '1', str(ip)]
        result= subprocess.run(command,capture_output=True)
        return result.returncode == 0
    
    @staticmethod
    def resolve_hostname(ip):
        """Resolve the hostname for a given IP address."""
        try:
            return socket.gethostbyaddr(str(ip))[0]
        except Exception:
            return "Unknown"
        
    @classmethod
    def scan_host(cls,ip):
        if not cls.ping(ip):
            return None
        return {
            'ip': str(ip),
            'hostname': cls.resolve_hostname(ip) if cls.resolve_hostname(ip) != "Unknown" else str(ip),
            'status': 'Online'
            }
    @classmethod
    def discover(cls):
        """Discover devices on the local network."""
        local_ip = cls.get_local_ip()
        network = ipaddress.ip_network(local_ip + '/24', strict=False)
        devices = []

        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(cls.scan_host, ip): ip for ip in network.hosts()}
            for future in as_completed(futures):
                device = future.result()
                if device:
                    devices.append(device)

        devices.sort(key=lambda x: x['ip'])

        return devices