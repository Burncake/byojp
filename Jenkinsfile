pipeline {
    agent any

    parameters {
        string(name: 'USER_ID', defaultValue: 'default-user', description: 'Your unique identifier (e.g., GitHub username)')
        string(name: 'WEBSITE_FILE', defaultValue: 'site1.html', description: 'The HTML file to display (site1.html, site2.html, or site3.html)')
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = "your-dockerhub-username/${params.USER_ID}-simple-webapp"
    }

    stages {
        stage('Build') {
            steps {
                echo "Building the Docker image for ${params.USER_ID}"
                script {
                    docker.build(DOCKER_IMAGE, "--build-arg WEBSITE_FILE=${params.WEBSITE_FILE} .")
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
                        docker.image(DOCKER_IMAGE).push("latest")
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    def allocatedPort = ""
                    wrap([$class: 'PortAllocator', port: 'DEPLOY_PORT', pool: 'default']) {
                        allocatedPort = env.DEPLOY_PORT
                    }
                    echo "Deploying container to port ${allocatedPort}"
                    sh "docker stop ${params.USER_ID}-webapp || true"
                    sh "docker rm ${params.USER_ID}-webapp || true"
                    sh "docker run -d --name ${params.USER_ID}-webapp -p ${allocatedPort}:5000 -e WEBSITE_FILENAME=${params.WEBSITE_FILE} ${DOCKER_IMAGE}"
                }
            }
        }
    }
}