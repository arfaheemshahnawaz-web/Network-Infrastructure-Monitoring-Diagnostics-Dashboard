from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeviceForm

# Create your views here.
from .models import (
    Device,
    HealthCheck,
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
