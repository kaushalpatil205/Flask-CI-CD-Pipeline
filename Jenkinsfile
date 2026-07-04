pipeline {
    agent any

    triggers {
        // Polls GitHub every 5 minutes for changes (or configure GitHub Webhook)
        pollSCM('H/5 * * * *')
    }

    environment {
        FLASK_APP = "app.py"
        FLASK_ENV = "testing"
    }

    stages {
        stage('Build: Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                '''
            }
        }

        stage('Test: Run Unit Tests') {
            steps {
                echo 'Running unit tests with pytest...'
                sh '''
                    . venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Deploy: Staging Environment') {
            when {
                branch 'main'
            }
            steps {
                echo 'Tests passed! Deploying application to staging environment...'
                sh '''
                    echo "Application successfully deployed to Staging Server!"
                    echo "Deployment Timestamp: $(date)"
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS: Build, Test, and Deployment completed successfully."
            // In a live server, you can use: mail to: 'devops-team@example.com', subject: 'Pipeline Success', body: 'The Jenkins pipeline executed successfully.'
        }
        failure {
            echo "FAILURE: Pipeline failed at stage: ${env.STAGE_NAME}."
            // In a live server, you can use: mail to: 'devops-team@example.com', subject: 'Pipeline Failed', body: 'Check Jenkins console logs.'
        }
    }
}
