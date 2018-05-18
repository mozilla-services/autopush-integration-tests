pipeline {
  agent {
      dockerfile {
        filename 'Dockerfile' 
        args '-u root:root' 
        additionalBuildArgs '--no-cache'
      }
  }
  libraries {
    lib('fxtest@1.9')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
  }
  environment {
    TEST_ENV = "${TEST_ENV ?: JOB_NAME.split('\\.')[1]}"
    SHAVAR_EMAIL_RECIPIENT = credentials('SHAVAR_EMAIL_RECIPIENT')
    GITHUB_ACCESS_TOKEN = credentials('GITHUB_ACCESS_TOKEN_RPAPA')
    SENTRY_TOKEN = credentials('SENTRY_TOKEN')
    HOST_SENTRY = credentials('HOST_SENTRY')
    HOST_UPDATES = 'updates-autopush.stage.mozaws.net'
  }
  stages {
    stage('Test Sentry check') {
      steps {
        script {
          sh "pytest --env='stage' tests/test_sentry.py -s"
        }
      } 
    }
  }
  post {
    success {
      emailext(
        body: 'Test summary: $BUILD_URL\n\n',
        replyTo: '$DEFAULT_REPLYTO',
        subject: "autopush ${env.TEST_ENV} succeeded!!",
        to: "${env.SHAVAR_EMAIL_RECIPIENT}")
    }
    failure {
      emailext(
        body: 'Test summary: $BUILD_URL\n\n',
        replyTo: '$DEFAULT_REPLYTO',
        subject: "autopush ${env.TEST_ENV} failed!",
        to: "${env.SHAVAR_EMAIL_RECIPIENT}")
    }
    changed {
      ircNotification('#fx-test-alerts')
    }
  }
}

