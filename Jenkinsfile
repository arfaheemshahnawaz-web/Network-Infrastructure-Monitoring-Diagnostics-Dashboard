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

        stage('Verify Environment') {
            steps {
                sh 'python3 --version'
                sh 'pip3 --version'
                sh 'git --version'
                sh 'docker --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Code Quality') {
            steps {
                sh 'ruff check .'
            }
        }

        stage('Django System Check') {
            steps {
                sh 'python3 manage.py check'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 manage.py test'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t network-monitor-dashboard:jenkins .'
            }
        }

    }

    post {

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }

        always {
            cleanWs()
        }
    }
}