pipeline {
    agent any

    environment {
        registry = "giantsweetroll/ripperdoc"
        registryCredential = 'dockerhub_token'
        dockerImage = ''
    }

    stages {
        stage("build") {
            steps {
                echo 'building the application....'
            }
        }

        stage("test") {
            steps {
                echo 'testing the application...'
            }
        }
        
        stage("Build Docker image") {
            steps {
                dir ("ripperdoc-backend") {
                    script {
                        dockerImage = docker.build registry
                    }
                }
            }
        }
        
        stage("Uploading Image") {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
                }
            }
        }

        stage("deploy") {
            steps {
                echo 'deploying the application...'
            }
        }
    }
}