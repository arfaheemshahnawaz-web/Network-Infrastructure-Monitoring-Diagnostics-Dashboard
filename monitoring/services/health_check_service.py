from monitoring.models import (
    HealthCheck,
    DNSCheck,
    PerformanceMetric,
    WiFiScan,
)

from monitoring.services.ping_service import ConnectivityTester
from monitoring.services.dns_service import DNSService
from monitoring.services.performance_service import PerformanceService
from monitoring.services.wifi_service import WiFiService


class HealthCheckService:

    @staticmethod
    def run_ping(device):

        tester = ConnectivityTester()

        result = tester.ping(device.ip_address)

        return HealthCheck.objects.create(
            device=device,
            status=result["status"],
            latency=result["avg_latency"]
            if result["avg_latency"] != "N/A"
            else 0,
            packet_loss=result["packet_loss"]
        )

    @staticmethod
    def run_dns(device):

        dns = DNSService()

        result = dns.resolve("google.com")

        return DNSCheck.objects.create(
            device=device,
            domain=result["domain"],
            resolved_ip=result["resolved_ip"],
            lookup_time=result["lookup_time"]
        )

    @staticmethod
    def run_performance(device):

        perf = PerformanceService()

        stats = perf.get_metrics()

        return PerformanceMetric.objects.create(
            device=device,
            cpu_usage=stats["cpu_usage"],
            memory_usage=stats["memory_usage"],
            bytes_sent=stats["bytes_sent"],
            bytes_received=stats["bytes_received"]
        )

    @staticmethod
    def run_wifi(device):

        WiFiScan.objects.filter(device=device).delete()

        networks = WiFiService.scan()

        for network in networks:

            WiFiScan.objects.create(
                device=device,
                ssid=network.get("ssid", ""),
                bssid=network.get("bssid", ""),
                signal=network.get("signal", 0),
                channel=network.get("channel", 0),
                band=network.get("band", ""),
                security=network.get("security", ""),
            )