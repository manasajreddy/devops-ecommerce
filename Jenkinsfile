

pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_IMAGE = "ecommerce-app"
    }

    stages {

        stage('Checkout Verification') {
            steps {
                echo 'Starting E-commerce CI/CD Pipeline'
                echo 'Repository checkout successful'

                sh 'pwd'
                sh 'ls -la'
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Project Verification') {
            steps {
                sh '''
                    test -f requirements.txt
                    test -f docker/Dockerfile
                    test -d app
                    test -d tests

                    echo "Project structure verified"
                '''
            }
        }

        stage('Install Dependencies and Test') {
            steps {
                sh '''
                    docker run --rm \
                      --volumes-from jenkins-server \
                      -w "$WORKSPACE" \
                      python:3.13-slim \
                      sh -c "python -m pip install --no-cache-dir -r requirements.txt && python -m pytest -v"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -f docker/Dockerfile \
                      -t ${APP_IMAGE}:${BUILD_NUMBER} \
                      .
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                sh '''
                    docker image inspect \
                      ${APP_IMAGE}:${BUILD_NUMBER}

                    docker images ${APP_IMAGE}
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: All CI stages completed!'
            echo 'Automated tests passed.'
            echo 'Docker image built successfully.'
        }

        failure {
            echo 'FAILURE: Check the Jenkins Console Output.'
        }

        always {
            echo 'CI Pipeline execution finished.'
        }
    }
}
