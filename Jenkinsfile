pipeline {
    agent any
    options { disableConcurrentBuilds() }
    triggers { pollSCM('H/5 * * * *') }
    stages {
        stage('Clean checkout') {
            steps { deleteDir(); checkout scm }
        }
        stage('Build image') {
            steps { sh 'docker build --pull -t aceest-jenkins:$BUILD_NUMBER .' }
        }
        stage('Syntax and lint') {
            steps {
                sh 'docker run --rm -e PYTHONPYCACHEPREFIX=/tmp/pycache aceest-jenkins:$BUILD_NUMBER python -m compileall -q app.py services.py tests'
                sh 'docker run --rm aceest-jenkins:$BUILD_NUMBER python -m ruff check --no-cache --select E9,F63,F7,F82 app.py services.py tests'
            }
        }
        stage('Tests') {
            steps { sh 'docker run --rm aceest-jenkins:$BUILD_NUMBER python -m pytest -q -p no:cacheprovider' }
        }
    }
    post {
        always { sh 'docker image rm aceest-jenkins:$BUILD_NUMBER || true' }
    }
}
