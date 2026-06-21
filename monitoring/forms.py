from django import forms
from .models import Device 

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['hostname', 'ip_address', 'device_type', 'os_type', 'location']