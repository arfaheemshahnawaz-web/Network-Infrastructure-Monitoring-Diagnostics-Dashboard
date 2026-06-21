from django.urls import path
from .views import (
    dashboard,
    device_list,
    add_device,
    edit_device,
    delete_device,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('devices/', device_list, name='device_list'),
    path('devices/add/', add_device, name='add_device'),
    path('devices/edit/<int:pk>/', edit_device, name='edit_device'),
    path('devices/delete/<int:pk>/', delete_device, name='delete_device'),
]
