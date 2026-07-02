# Jenkins Setup

This directory contains the configuration required to run a local Jenkins server using Docker.

The Jenkins instance is used to demonstrate a complete CI pipeline for the Network Infrastructure Monitoring & Diagnostics Dashboard project.

## Features

- Jenkins LTS (JDK 21)
- Python 3
- Git
- Docker CLI
- Docker socket access for building Docker images
- Pipeline support using the project's `Jenkinsfile`

## Requirements

- Docker Desktop
- Docker Compose

## Start Jenkins

```bash
cd jenkins
docker compose up --build -d
```

Jenkins will be available at:

```
http://localhost:8080
```

## Stop Jenkins

```bash
docker compose down
```

## Initial Setup

After starting Jenkins for the first time:

1. Unlock Jenkins using the initial administrator password.
2. Install the suggested plugins.
3. Create an administrator account.

## Create the Pipeline

Create a new **Pipeline** job.

Pipeline configuration:

- **Definition:** Pipeline script from SCM
- **SCM:** Git
- **Repository URL:**

```
https://github.com/arfaheemshahnawaz-web/Network-Infrastructure-Monitoring-Diagnostics-Dashboard.git
```

- **Branch:**

```
*/main
```

- **Script Path:**

```
Jenkinsfile
```

Disable **Lightweight checkout** before saving.

## Pipeline Stages

The Jenkins pipeline performs:

- Repository checkout
- Python virtual environment creation
- Dependency installation
- Ruff linting
- Django system checks
- Test execution
- Docker image build
- Workspace cleanup

## Files

```
jenkins/
├── Dockerfile
├── docker-compose.yml
└── README.md
```