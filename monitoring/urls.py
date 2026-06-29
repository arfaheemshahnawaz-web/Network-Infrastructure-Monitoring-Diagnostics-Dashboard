from django.urls import path
from .views import (
    dashboard,
    device_list,
    add_device,
    dns_check_history,
    edit_device,
    delete_device,
    run_dns_check,
    run_ping_check,
    health_check_history,
    run_performance_check,
    performance_history,
    system_info,
    device_detail,
    run_wifi_scan
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('devices/', device_list, name='device_list'),
    path('devices/add/', add_device, name='add_device'),
    path('devices/edit/<int:pk>/', edit_device, name='edit_device'),
    path('devices/delete/<int:pk>/', delete_device, name='delete_device'),
    path('devices/ping/<int:pk>/', run_ping_check, name='run_ping_check'),
    path('devices/history/', health_check_history, name='health_check_history'),
    path('devices/dns_check/<int:pk>/', run_dns_check, name='run_dns_check'),
    path('devices/dns_history/', dns_check_history, name='dns_check_history'),
    path('devices/performance/<int:pk>/',run_performance_check,name="run_performance_check" ),
    path('devices/performance_history/',performance_history,name="performance_history"),
    path('devices/system_info/',system_info, name="system_info"),
    path("devices/<int:pk>/",device_detail,name="device_detail",),
    path(
    "devices/<int:pk>/wifi/",run_wifi_scan,name="run_wifi_scan",),
]
