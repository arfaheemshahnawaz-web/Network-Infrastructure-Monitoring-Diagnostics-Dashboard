# Network Infrastructure Monitoring & Diagnostics Dashboard

[![Django CI](https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard/actions/workflows/ci.yml)

A production-style Django application that demonstrates infrastructure monitoring, network diagnostics, backend development, and modern DevOps practices.

The project performs network diagnostics, monitors device health, stores monitoring data in PostgreSQL, executes scheduled background tasks using Celery, and provides infrastructure metrics through Prometheus and Grafana.

The application uses Docker, Docker Compose, Nginx, PostgreSQL, Redis, Celery, Prometheus, Grafana, Jenkins, and GitHub Actions.

---

# Features

## Device Management

- Add, Edit and Delete Devices
- Device Inventory
- Device Details
- Device Status Tracking
- Device IP and MAC Address Information

## Device Discovery

- Automatic local network discovery
- ICMP-based device reachability detection
- Hostname resolution
- MAC address detection using the host network agent
- Automatic saving of discovered devices to PostgreSQL
- Existing devices are updated instead of creating duplicates

## Monitoring Dashboard

- Total Devices
- Online Devices
- Offline Devices
- Recent Health Checks
- Current Device Status
- Latency Information
- Packet Loss Information

## Network Diagnostics

- ICMP Ping Diagnostics
- Device Reachability Checks
- Packet Loss Measurement
- Average Latency Measurement
- Health Check History

## DNS Monitoring

- Domain Resolution
- DNS Lookup Time Measurement
- DNS History

## System Diagnostics

- System Information
- Network Interface Information
- Default Gateway Information
- DNS Server Information
- CPU Usage Monitoring
- Memory Usage Monitoring
- Disk Usage Monitoring
- Network Traffic Statistics

## Wi-Fi Diagnostics

Collects nearby wireless network information using native operating system utilities:

- **Windows:** `netsh`
- **Linux:** `nmcli`

The available Wi-Fi information depends on the underlying operating system and wireless adapter capabilities.

When running inside Docker, Wi-Fi scanning is skipped gracefully if the required native utility is unavailable inside the container.

## Infrastructure Monitoring

- Prometheus Metrics Collection
- Grafana Dashboards
- Docker Container Monitoring using cAdvisor
- Host System Monitoring using Node Exporter
- Django Application Metrics

## Background Monitoring

- Celery Worker
- Celery Beat
- Redis Message Broker
- Scheduled Health Checks
- Automatic Ping Health Checks
- Automatic DNS Checks
- Automatic Performance Checks
- Wi-Fi Diagnostics with graceful failure handling

## Diagnostic History

- Health Check History
- DNS Check History
- Performance History
- Wi-Fi Scan History

---

# Current Implementation

The application currently monitors **the host machine on which the monitoring server is running**.

- Device records represent monitored endpoints.
- System diagnostics are collected from the monitoring host.
- Network diagnostics execute from the monitoring host.
- Discovered devices are stored in PostgreSQL.
- Device status is updated through health checks.
- Background monitoring is performed using Celery and Celery Beat.

For Windows-based environments, a lightweight host network agent provides ARP/MAC address information to the Dockerized application.

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
- Django Celery Beat

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

## Networking

- TCP/IP
- ICMP
- DNS
- ARP
- Wi-Fi diagnostics
- Network interface monitoring

---

# Architecture

```text
                         Grafana
                            │
                            ▼
                       Prometheus
                    /       │       \
                   /        │        \
                  ▼         ▼         ▼
          Node Exporter  cAdvisor  Django Metrics
                                      │
                                      ▼
                                    Nginx
                                      │
                                      ▼
                                  Gunicorn
                                      │
                                      ▼
                                   Django
                              /       │       \
                             ▼        ▼        ▼
                        PostgreSQL  Redis   Celery Worker
                                          │
                                          ▼
                                      Celery Beat


                 Windows Host Network Agent
                           │
                           │ ARP / MAC
                           ▼
                        Django
```

## Monitoring Workflow

```text
Network Discovery
       │
       ▼
Find Reachable Devices
       │
       ▼
IP + Hostname + MAC
       │
       ▼
Save / Update Device
       │
       ▼
PostgreSQL
       │
       ▼
Celery Beat
       │
       ▼
Scheduled Health Checks
       │
       ├── Ping
       ├── DNS
       ├── Performance
       └── Wi-Fi
       │
       ▼
HealthCheck / Diagnostic History
       │
       ▼
Dashboard + Grafana
```

---

# Networking Concepts Demonstrated

- TCP/IP Fundamentals
- ICMP (Ping)
- DNS Resolution
- ARP
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
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── ...
│
├── monitoring/
│   ├── services/
│   │   ├── discover_service.py
│   │   ├── dns_service.py
│   │   ├── health_check_service.py
│   │   ├── interface_service.py
│   │   ├── performance_service.py
│   │   ├── ping_service.py
│   │   ├── system_info.py
│   │   └── wifi_service.py
│   │
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── tasks.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── monitoring-stack/
│   └── prometheus/
│       └── prometheus.yml
│
├── nginx/
│   └── nginx.conf
│
├── jenkins/
│
├── .github/
│   └── workflows/
│
├── setup_network.py
├── host_network_agent.py
├── docker-compose.yml
├── Dockerfile
├── entrypoint-web.sh
├── entrypoint-worker.sh
├── entrypoint-beat.sh
├── .env
├── .env.docker
├── .env.docker.local
├── manage.py
└── requirements.txt
```

---

# Environment Configuration

The project uses environment-specific configuration files.

## `.env`

Used for local Django development.

## `.env.docker`

Used for Docker Compose configuration.

## `.env.docker.local`

Used for machine-specific network configuration.

This file is generated automatically by:

```bash
python setup_network.py
```

Example:

```env
DISCOVERY_NETWORK=192.168.1.0/24
DISCOVERY_AGENT_HOST=192.168.1.7
DISCOVERY_AGENT_PORT=8765
```

The local network configuration file should not be committed because the values depend on the machine and network where the project is running.

---

# Network Setup

Run:

```bash
python setup_network.py
```

The script detects the local LAN IP and generates `.env.docker.local`.

The Windows network agent can then be started using:

```bash
python host_network_agent.py
```

The agent exposes ARP information to the Dockerized application.

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

## Configure Local Network

Run:

```bash
python setup_network.py
```

This creates:

```
.env.docker.local
```

## Start the Host Network Agent

```bash
python host_network_agent.py
```

## Start Docker Services

```bash
docker compose up --build -d
```

For normal subsequent starts:

```bash
docker compose up -d
```

---

# Services

| Service | URL |
|---------|-----|
| Django Application | http://localhost |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |

---

# Scheduled Monitoring

Celery Beat schedules the health-check task using Django Celery Beat.

The task:

```
monitoring.tasks.run_all_health_checks
```

runs periodically and performs:

- Ping
- DNS
- Performance
- Wi-Fi

Health-check results are stored in PostgreSQL.

The current device status is also updated based on the latest ping result.

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

# Learning Objectives

This project demonstrates practical experience with:

- Python Backend Development
- Django
- Infrastructure Monitoring
- Network Diagnostics
- Linux Networking Concepts
- TCP/IP & ICMP Diagnostics
- DNS Resolution
- ARP
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

GitHub: [https://github.com/arfaheemshahnawaz-web](https://github.com/arfaheemshahnawaz-web)

LinkedIn: [https://www.linkedin.com/in/a-r-faheem-shah-nawaz](https://www.linkedin.com/in/a-r-faheem-shah-nawaz)