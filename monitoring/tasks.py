from celery import shared_task

from monitoring.models import Device
from monitoring.services.health_check_service import HealthCheckService


@shared_task
def run_all_health_checks():

    devices = Device.objects.all()

    for device in devices:

        HealthCheckService.run_ping(device)
        HealthCheckService.run_dns(device)
        HealthCheckService.run_performance(device)
        HealthCheckService.run_wifi(device)