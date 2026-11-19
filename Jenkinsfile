pipeline {
    agent any

    environment {
        PLAYWRIGHT_BROWSERS_PATH = '/ms-playwright'
    }

    stages {
        stage('Run tests') {
            steps {
                sh 'pytest || true'
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
            jdk: '',
            results: [[path: 'allure-results']]
        }
    }
}
