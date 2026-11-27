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
        stage('Code Quality (Ruff)') {
            steps {
                sh 'ruff check .'
            }
        }

        stage('Run tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    script {
                        def marker = params.TEST_SUITE == 'all' ? '' : "-m ${params.TEST_SUITE}"
                        sh "pytest ${marker}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('allure-results')) {
                    allure includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                }
            }
        }
    }
}
