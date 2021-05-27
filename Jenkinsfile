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
        
        stage('Stop Container') {
         steps {
            echo 'Stop container if running'
            sh 'docker ps -f name=ripperdoc-backend -q | xargs --no-run-if-empty docker container stop'
            sh 'docker container ls -a -fname=ripperdoc-backend -q | xargs -r docker container rm'
         }
       }
        
        stage("Run and Test Image") {
            steps {
                echo 'Running docker image...'
                script {
                    sh 'docker container ls'
                    dockerImage.inside ('--entrypoint "" -p 5000:5000 --name ripperdoc-backend --rm') {
                        // Test container here
                        sh 'ls'
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