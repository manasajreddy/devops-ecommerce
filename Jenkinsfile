


pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'ecommerce-app'
    }

    stages {

        stage('Checkout Verification') {
            steps {
                echo 'Checking out the source code'
                sh 'git status --short'
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Automated Testing') {
            steps {
                sh '''
                    set -eu

                    TEST_CONTAINER="ecommerce-test-${BUILD_NUMBER}"

                    docker rm -f "$TEST_CONTAINER" >/dev/null 2>&1 || true

                    docker create \
                        --name "$TEST_CONTAINER" \
                        -w /workspace \
                        python:3.13-slim sleep infinity

                    docker cp "$WORKSPACE/." "$TEST_CONTAINER:/workspace"

                    docker start "$TEST_CONTAINER"

                    docker exec "$TEST_CONTAINER" sh -c \
                      "python -m pip install --no-cache-dir -r requirements.txt && python -m pytest -v"

                    docker rm -f "$TEST_CONTAINER"
                '''
            }
        }

        stage('Docker Image Build') {
            steps {
                sh '''
                    set -eu
                    docker build \
                        -f docker/Dockerfile \
                        -t ecommerce-app:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Container Deployment Test') {
            steps {
                sh '''
                    set -eu

                    APP_CONTAINER="ecommerce-ci-${BUILD_NUMBER}"

                    docker rm -f "$APP_CONTAINER" >/dev/null 2>&1 || true

                    docker run -d \
                        --name "$APP_CONTAINER" \
                        -p 18080:8080 \
                        ecommerce-app:${BUILD_NUMBER}

                    sleep 5

                    docker exec "$APP_CONTAINER" python -c \
                      "import urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=10); print(r.status, r.read().decode()); assert r.status == 200"

                    docker rm -f "$APP_CONTAINER"
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f "ecommerce-test-${BUILD_NUMBER}" >/dev/null 2>&1 || true
                docker rm -f "ecommerce-ci-${BUILD_NUMBER}" >/dev/null 2>&1 || true
            '''
        }

        success {
            echo 'CI PIPELINE SUCCESSFUL: Tests passed, image built and container health verified.'
        }

        failure {
            echo 'CI PIPELINE FAILED: Check the failed stage in Console Output.'
        }
    }
}