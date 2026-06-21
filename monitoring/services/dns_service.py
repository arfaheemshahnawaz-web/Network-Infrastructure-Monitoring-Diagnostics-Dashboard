import socket
import time


class DNSService:

    @staticmethod
    def resolve(domain):
        start = time.time()
        try:
            ip = socket.gethostbyname(
                domain
            )
            status = "success"

        except Exception:
            ip = "Resolution Failed"
            status = "failed"
        end = time.time()
        lookup_time = round(
            (end - start) * 1000,
            2
        )
        
        return {
            "domain": domain,
            "resolved_ip": ip,
            "lookup_time": lookup_time,
            "status": status
        }