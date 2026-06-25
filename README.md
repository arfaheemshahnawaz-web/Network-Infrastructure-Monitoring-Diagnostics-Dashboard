# Network Infrastructure Monitoring & Diagnostics Dashboard

A Django-based infrastructure monitoring platform designed to demonstrate networking, system monitoring, diagnostics, and backend engineering concepts.

## Features Implemented

### Device Management

* Add Devices
* Edit Devices
* Delete Devices
* View Device Inventory

### Dashboard

* Total Devices
* Online Devices
* Offline Devices

### Network Health Monitoring

* ICMP Ping Diagnostics
* Device Reachability Checks
* Packet Loss Measurement
* Average Latency Measurement

### DNS Monitoring

* Domain Resolution Checks
* DNS Lookup Time Measurement
* Historical DNS Records

### Diagnostic History

* Health Check History
* DNS Check History

## Technology Stack

* Python
* Django
* SQLite (temporary)
* Git
* GitHub

## Networking Concepts Demonstrated

* TCP/IP Fundamentals
* ICMP (Ping)
* DNS Resolution
* Network Reachability Testing
* Latency Analysis
* Packet Loss Monitoring

## Project Structure

```text
monitoring/
├── services/
│   ├── ping_service.py
│   └── dns_service.py
├── models.py
├── views.py
├── forms.py
├── urls.py
└── templates/
```

## Current Status

Completed:

* Device CRUD
* Dashboard
* Ping Diagnostics
* DNS Diagnostics
* Diagnostic History Pages

Planned:

* Performance Monitoring (CPU, Memory, Network Usage)
* Linux Interface Diagnostics
* Wi-Fi Diagnostics
* PostgreSQL Migration
* Redis Integration
* Celery Background Tasks
* Docker Containerization
* Nginx Reverse Proxy
* Jenkins CI/CD Pipeline
* AWS Deployment
* Terraform Infrastructure Provisioning
* Ansible Configuration Management
* Kubernetes Deployment

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Learning Objectives

This project is being built to demonstrate practical experience with:

* Linux System Programming
* Networking Fundamentals
* Infrastructure Monitoring
* Backend Development
* DevOps Tooling
* Cloud Deployment
