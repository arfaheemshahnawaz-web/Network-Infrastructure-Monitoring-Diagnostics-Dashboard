from django.contrib import admin

# Register your models here.
from .models import (
    Device, 
    HealthCheck, 
    DNSCheck, 
    PerformanceMetric, 
    WiFiScan
)

admin.site.register(Device)
admin.site.register(HealthCheck)
admin.site.register(DNSCheck)
admin.site.register(PerformanceMetric)
admin.site.register(WiFiScan)
