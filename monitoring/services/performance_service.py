import psutil

class PerformanceService:

    @staticmethod
    def get_metrics():
        network = psutil.net_io_counters()
        return{
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv,
        }