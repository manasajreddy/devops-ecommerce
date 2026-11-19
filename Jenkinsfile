
pipeline {
    agent any

    options {
        timestamps()
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

        stage('Pipeline Status') {
            steps {
                echo 'Source code is ready for the next CI/CD stages.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
