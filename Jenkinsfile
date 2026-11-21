pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'ui', 'api'],
            description: 'Select tests to run'
        )
    }

    environment {
        PLAYWRIGHT_BROWSERS_PATH = '/ms-playwright'
    }

    stages {
        stage('Run tests') {
            steps {
                script {
                    def marker = params.TEST_SUITE == 'all' ? '' : "-m ${params.TEST_SUITE}"
                    sh "pytest ${marker} || true"
                }
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
