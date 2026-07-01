# Network Infrastructure Monitoring & Diagnostics Dashboard

[![Django CI](https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard/actions/workflows/ci.yml)

A production-style Django application that demonstrates infrastructure monitoring, network diagnostics, backend development, and modern DevOps practices. The project monitors network devices, performs health checks, and showcases containerized deployment using Docker, Nginx, PostgreSQL, Redis, Celery, and GitHub Actions.

---

## Features

### Device Management

- Add, Edit and Delete Devices
- Device Inventory Dashboard

### Monitoring Dashboard

- Total Devices
- Online Devices
- Offline Devices

### Network Diagnostics

- ICMP Ping Diagnostics
- Device Reachability Checks
- Packet Loss Measurement
- Average Latency Measurement

### DNS Monitoring

- Domain Resolution
- DNS Lookup Time Measurement
- DNS History

### System Diagnostics

- System Information
- Network Interface Information

### Diagnostic History

- Health Check History
- DNS Check History

---

## Technology Stack

### Backend

- Python 3.12
- Django 5
- Gunicorn

### Database

- PostgreSQL

### Background Processing

- Celery
- Redis
- Celery Beat

### Web Server

- Nginx

### Containerization

- Docker
- Docker Compose

### DevOps

- Git
- GitHub
- GitHub Actions (CI)

---

## Architecture

```
                    Nginx
                      │
                      ▼
                 Gunicorn
                      │
                      ▼
                  Django App
                 /     |      \
                /      |       \
               ▼       ▼        ▼
        PostgreSQL   Redis   Celery Worker
                         │
                         ▼
                   Celery Beat
```

---

## Networking Concepts Demonstrated

- TCP/IP Fundamentals
- ICMP (Ping)
- DNS Resolution
- Network Reachability
- Packet Loss Analysis
- Network Latency Monitoring
- Interface Diagnostics

---

## Project Structure

```
.
├── config/
├── monitoring/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   ├── urls.py
│   └── forms.py
├── nginx/
├── .github/
│   └── workflows/
├── docker-compose.yml
├── Dockerfile
├── entrypoint-web.sh
├── entrypoint-worker.sh
├── entrypoint-beat.sh
├── manage.py
└── requirements.txt
```

---

## Running the Project

### Clone the repository

```bash
git clone https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard.git

cd Network-Infrastructure-Monitoring-Diagnostics-Dashboard
```

### Configure Environment Variables

Create a `.env.docker` file:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=network_monitor

DB_USER=postgres

DB_PASSWORD=postgres

DB_HOST=db

DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0

CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### Run using Docker

```bash
docker compose up --build
```

The application will be available at:

```
http://localhost
```

---

## CI Pipeline

GitHub Actions automatically performs:

- Dependency Installation
- Ruff Linting
- Django System Checks
- Docker Image Build

---

## Current Status

### Completed

- Device CRUD
- Dashboard
- Ping Diagnostics
- DNS Diagnostics
- System Information
- Interface Diagnostics
- PostgreSQL Integration
- Redis Integration
- Celery Worker
- Celery Beat Scheduler
- Docker Containerization
- Nginx Reverse Proxy
- GitHub Actions CI Pipeline

### Planned

- CPU & Memory Monitoring
- Network Traffic Monitoring
- Scheduled Health Checks
- Email Notifications
- Jenkins Deployment Pipeline
- Terraform Infrastructure
- Ansible Automation
- Kubernetes Deployment
- Cloud Deployment

---

## Learning Objectives

This project demonstrates practical experience with:

- Django Backend Development
- REST-Oriented Backend Design
- Linux Networking Concepts
- Infrastructure Monitoring
- Docker & Docker Compose
- Nginx Reverse Proxy
- PostgreSQL
- Redis
- Celery & Background Tasks
- GitHub Actions CI
- DevOps Fundamentals
- Cloud Deployment Concepts

---

## Author

**A R Faheem Shah Nawaz**

GitHub: https://github.com/arfaheemshahnawaz-web

LinkedIn: https://www.linkedin.com/in/a-r-faheem-shah-nawaz