pipeline {
    agent any

    environment {
        registry = "giantsweetroll/ripperdoc"
        registryCredential = 'dockerhub_token'
        dockerImage = ''
    }

    stages {
        stage("Build Docker image") {
            steps {
                echo 'building docker image...'
                dir ("ripperdoc-backend") {
                    script {
                        dockerImage = docker.build registry + ':backend'
                    }
                }
                echo 'docker image built!'
            }
        }
        
        stage("Test Image") {
            steps {
                echo 'Running docker image...'
                script {
                    dockerImage.inside ('-p 5000:5000 --name ripperdoc-backend --rm') {
                        // Test container here
                        sh 'python --version'
                    }
                }
                echo 'Docker image ran and was tested successfully'
            }
        }
        
        stage("Uploading Image") {
            steps {
                echo 'Pushing image to docker hub...'
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
                }
                echo 'Docker image successfully pushed to Docker Hub!'
            }
        }

        stage("deploy") {
            steps {
                echo 'deploying the application...'
            }
        }
    }
}