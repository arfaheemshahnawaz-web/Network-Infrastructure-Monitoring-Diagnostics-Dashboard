from django.db import models

# Create your models here.
class Device(models.Model):
    DEVICE_TYPES = [
        ('server', 'Server'),
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('ap', 'Access Point'),
        ('workstation', 'Workstation'),
    ]

    hostname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    os_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hostname
    
class HealthCheck(models.Model):

    status_choices = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status_choices)
    latency = models.FloatField()
    packet_loss = models.FloatField()
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.hostname} - {self.status}"
    
class DNSCheck(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)
    resolved_ip = models.CharField(max_length=100)
    lookup_time = models.FloatField()
    checked_at = models.DateTimeField(auto_now_add=True)

class PerformanceMetric(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    bytes_sent = models.BigIntegerField()
    bytes_received = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class WiFiScan(models.Model):

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE
    )

    ssid = models.CharField(max_length=100)

    bssid = models.CharField(
        max_length=50,
        default="",
        blank=True
    )

    signal = models.IntegerField(
        default=0
    )

    channel = models.IntegerField(
        default=0
    )

    band = models.CharField(
        max_length=20,
        default="",
        blank=True
    )

    security = models.CharField(
        max_length=50,
        default="",
        blank=True
    )

    scanned_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.device.hostname} - {self.ssid}"