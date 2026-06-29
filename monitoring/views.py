from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeviceForm
from monitoring.services.ping_service import ConnectivityTester  
from monitoring.services.dns_service import DNSService 
from monitoring.services.performance_service import PerformanceService
from monitoring.services.system_info import SystemInfoService
from monitoring.services.interface_service import InterfaceService
from monitoring.services.wifi_service import WiFiService

# Create your views here.
from .models import (
    Device,
    HealthCheck,
    DNSCheck,
    PerformanceMetric,
    WiFiScan
)

def dashboard(request):
    total_devices = Device.objects.count()
    online_devices = HealthCheck.objects.filter(status='online').count()
    offline_devices = HealthCheck.objects.filter(status='offline').count()
    context = {
        'total_devices': total_devices,
        'online_devices': online_devices,
        'offline_devices': offline_devices,
    }
    return render(request, 'monitoring/dashboard.html', context)

def device_list(request):
    devices = Device.objects.all()
    
    return render(request, 'monitoring/device_list.html', {'devices': devices})

def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm()
    
    return render(request, 'monitoring/add_device.html', {'form': form})

def edit_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_list')
        
    else:
        form = DeviceForm(instance=device)

    return render(request, 'monitoring/edit_device.html', {'form': form})


def delete_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    
    return render(request, 'monitoring/delete_device.html', {'device': device})

def run_ping_check(request, pk):
    device = get_object_or_404(Device, pk=pk)
    tester = ConnectivityTester()
    result = tester.ping(device.ip_address)

    # Save the result to HealthCheck model
    HealthCheck.objects.create(
        device=device,
        status=result['status'],
        latency=result['avg_latency']
        if result['avg_latency'] != "N/A" else 0,
        packet_loss=result['packet_loss']
    )

    return redirect('device_list')

def health_check_history(request):

    checks=(HealthCheck.objects.select_related('device').order_by("-checked_at"))
    return render(request, 'monitoring/health_check_history.html', {'checks': checks})


def run_dns_check(request, pk):
    device = get_object_or_404(Device, pk=pk)
    dns_service = DNSService()
    result = dns_service.resolve("google.com")  # Example domain(change later)

    # Save the result to DNSCheck model
    DNSCheck.objects.create(
        device=device,
        domain=result['domain'],
        resolved_ip=result['resolved_ip'],
        lookup_time=result['lookup_time']
    )

    return redirect('device_list')

def dns_check_history(request):
    records = DNSCheck.objects.select_related('device').order_by("-checked_at")
    return render(request, 'monitoring/dns_history.html', {'records': records})

def run_performance_check(request, pk):
    device = get_object_or_404(Device, pk=pk)
    metrics = PerformanceService.get_metrics()
    PerformanceMetric.objects.create(
        device=device,
        cpu_usage= metrics["cpu_usage"],
        memory_usage=metrics["memory_usage"],
        bytes_sent=metrics['bytes_sent'],
        bytes_received=metrics['bytes_received'],
    )

    return redirect("device_list")

def performance_history(request):
    metrics=PerformanceMetric.objects.select_related('device').order_by('-timestamp')
    return render(request, 'monitoring/performance_history.html',{"metrics":metrics})

def system_info(request):
    info = SystemInfoService.get_info()
    return render(
        request,'monitoring/system_info.html',{"info":info}
    )

def device_detail(request, pk):

    device = get_object_or_404(Device, pk=pk)
    system_info= SystemInfoService.get_info()
    interfaces = InterfaceService.get_interfaces()
    gateway = InterfaceService.get_default_gateway()
    dns_servers = InterfaceService.get_dns_servers()
    wifi_networks = (WiFiScan.objects.filter(device=device).order_by("-signal"))
    

    latest_ping = (
        HealthCheck.objects
        .filter(device=device)
        .order_by("-checked_at")
        .first()
    )

    latest_dns = (
        DNSCheck.objects
        .filter(device=device)
        .order_by("-checked_at")
        .first()
    )

    latest_performance = (
        PerformanceMetric.objects
        .filter(device=device)
        .order_by("-timestamp")
        .first()
    )

    context = {
        "device": device,
        "latest_ping": latest_ping,
        "latest_dns": latest_dns,
        "latest_performance": latest_performance,
        "system_info": system_info,
        "interfaces": interfaces,
        "gateway": gateway,
        "dns_servers": dns_servers,
        "wifi_networks": wifi_networks,
    }

    return render(
        request,
        "monitoring/device_detail.html",
        context,
    )

def run_wifi_scan(request, pk):

    device = get_object_or_404(Device, pk=pk)

    networks = WiFiService.scan()

    # Remove previous scan results
    WiFiScan.objects.filter(device=device).delete()

    # Save latest scan
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

    return redirect("device_detail", pk=device.pk)