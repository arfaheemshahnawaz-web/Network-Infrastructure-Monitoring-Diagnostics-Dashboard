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

        health_check = HealthCheck.objects.create(
            device=device,
            status=result["status"],
            latency=(
                float(result["avg_latency"])
                if result["avg_latency"] != "N/A"
                else 0
            ),
            packet_loss=float(result["packet_loss"])
        )

        # Update current device status
        device.status = result["status"]
        device.save(update_fields=["status"])

        return health_check

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

        try:
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

        except FileNotFoundError:
            print("Wi-Fi scan skipped: nmcli is not available in the container.")

        except Exception as e:
            print(f"Wi-Fi scan failed: {e}")