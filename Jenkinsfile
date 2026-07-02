pipeline {
    agent any

    environment {
        SECRET_KEY = 'test-secret-key'
        DEBUG = 'True'

        DB_NAME = 'test_db'
        DB_USER = 'postgres'
        DB_PASSWORD = 'postgres'
        DB_HOST = 'localhost'
        DB_PORT = '5432'

        CELERY_BROKER_URL = 'redis://localhost:6379/0'
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    ruff check .
                '''
            }
        }

        stage('Django System Check') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py check
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t network-monitor-dashboard:jenkins .
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}