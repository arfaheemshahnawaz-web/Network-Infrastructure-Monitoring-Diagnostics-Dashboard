# Network Infrastructure Monitoring & Diagnostics Dashboard

[![Django CI](https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard/actions/workflows/ci.yml)

A production-style Django application that demonstrates infrastructure monitoring, network diagnostics, backend development, and modern DevOps practices. The project performs network diagnostics, monitors system health, executes background monitoring tasks, and showcases containerized deployment using Docker, Nginx, PostgreSQL, Redis, Celery, Prometheus, Grafana, Jenkins, and GitHub Actions.

---

# Features

## Device Management

- Add, Edit and Delete Devices
- Device Inventory Dashboard
- Device Details

## Monitoring Dashboard

- Total Devices
- Online Devices
- Offline Devices

## Network Diagnostics

- ICMP Ping Diagnostics
- Device Reachability Checks
- Packet Loss Measurement
- Average Latency Measurement

## DNS Monitoring

- Domain Resolution
- DNS Lookup Time Measurement
- DNS History

## System Diagnostics

- System Information
- Network Interface Information
- CPU Usage Monitoring
- Memory Usage Monitoring
- Disk Usage Monitoring

## Wi-Fi Diagnostics

Collects nearby wireless network information using native operating system utilities:

- **Windows:** `netsh`
- **Linux:** `nmcli`

The available Wi-Fi information depends on the underlying operating system and wireless adapter capabilities.

## Infrastructure Monitoring

- Prometheus Metrics Collection
- Grafana Dashboards
- Docker Container Monitoring (cAdvisor)
- Host System Monitoring (Node Exporter)

## Diagnostic History

- Health Check History
- DNS Check History
- Performance History

---

# Current Implementation

The application currently monitors **the host machine on which the monitoring server is running**.

- Device records represent monitored endpoints.
- System diagnostics are collected from the monitoring host.
- Network diagnostics execute from the monitoring host.

Future versions can be extended with:

- Remote monitoring agents
- SSH-based monitoring
- Distributed infrastructure monitoring

---

# Technology Stack

## Backend

- Python 3.12
- Django 5
- Gunicorn

## Database

- PostgreSQL

## Background Processing

- Celery
- Celery Beat
- Redis

## Reverse Proxy

- Nginx

## Monitoring

- Prometheus
- Grafana
- Node Exporter
- cAdvisor

## Containerization

- Docker
- Docker Compose

## CI/CD

- GitHub Actions
- Jenkins

---

# Architecture

```
                        Grafana
                           │
                           ▼
                     Prometheus
                    /     |      \
                   /      |       \
                  ▼       ▼        ▼
          Node Exporter cAdvisor Django Metrics
                                   │
                                   ▼
                              Nginx
                                │
                                ▼
                           Gunicorn
                                │
                                ▼
                             Django
                        /       |        \
                       ▼        ▼         ▼
                 PostgreSQL   Redis   Celery Worker
                                     │
                                     ▼
                                Celery Beat
```

---

# Networking Concepts Demonstrated

- TCP/IP Fundamentals
- ICMP (Ping)
- DNS Resolution
- Network Reachability
- Packet Loss Analysis
- Network Latency Monitoring
- Network Interface Diagnostics
- Wi-Fi Network Discovery
- Host System Monitoring

---

# Project Structure

```
.
├── config/
├── monitoring/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── tasks.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── monitoring-stack/
│   └── prometheus/
│       └── prometheus.yml
├── nginx/
├── .github/
│   └── workflows/
├── jenkins/
├── docker-compose.yml
├── Dockerfile
├── entrypoint-web.sh
├── entrypoint-worker.sh
├── entrypoint-beat.sh
├── .env
├── .env.docker
├── manage.py
└── requirements.txt
```

---

# Environment Configuration

The project uses two environment files:

## `.env`

Used for **local Django development**.

## `.env.docker`

Used when running the application using Docker Compose.

Typical variables include:

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

---

# Entrypoint Scripts

The project uses dedicated entrypoint scripts for each service.

### entrypoint-web.sh

- Waits for PostgreSQL
- Applies database migrations
- Collects static files
- Starts Gunicorn

### entrypoint-worker.sh

- Waits for PostgreSQL
- Starts the Celery Worker

### entrypoint-beat.sh

- Waits for PostgreSQL
- Starts Celery Beat Scheduler

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard.git

cd Network-Infrastructure-Monitoring-Diagnostics-Dashboard
```

## Start the Application

```bash
docker compose up --build
```

---

# Services

| Service | URL |
|---------|-----|
| Django Application | http://localhost |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |

---

# CI/CD

## GitHub Actions

Automatically performs:

- Dependency Installation
- Ruff Linting
- Django System Checks
- Docker Image Build

## Jenkins

A Jenkins pipeline is included to demonstrate CI automation and Docker image builds.

---

# Current Status

## Completed

- Device CRUD
- Dashboard
- Ping Diagnostics
- DNS Diagnostics
- Performance Monitoring
- System Information
- Wi-Fi Diagnostics
- Diagnostic History
- PostgreSQL Integration
- Redis Integration
- Celery Worker
- Celery Beat Scheduler
- Docker Containerization
- Gunicorn
- Nginx Reverse Proxy
- Prometheus Integration
- Grafana Dashboards
- Node Exporter
- cAdvisor
- GitHub Actions CI
- Jenkins Pipeline

## Future Improvements

- Scheduled Health Checks
- Email Notifications
- Additional Grafana Dashboards
- Remote Agent Monitoring
- SSH-Based Monitoring

---

# Learning Objectives

This project demonstrates practical experience with:

- Python Backend Development
- Django
- Infrastructure Monitoring
- Linux Networking Concepts
- TCP/IP & ICMP Diagnostics
- DNS Resolution
- Wi-Fi Diagnostics
- Docker & Docker Compose
- Gunicorn
- Nginx Reverse Proxy
- PostgreSQL
- Redis
- Celery
- Prometheus
- Grafana
- Jenkins
- GitHub Actions
- CI/CD Practices

---

# Author

**A R Faheem Shah Nawaz**

GitHub: https://github.com/arfaheemshahnawaz-web

LinkedIn: https://www.linkedin.com/in/a-r-faheem-shah-nawaz