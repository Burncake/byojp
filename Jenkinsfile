pipeline {
    agent any

    parameters {
        string(name: 'USER_ID', defaultValue: 'default-user', description: 'Your unique identifier (e.g., GitHub username)')
        string(name: 'WEBSITE_FILE', defaultValue: 'site1.html', description: 'The HTML file to display (site1.html, site2.html, or site3.html)')
    }

    environment {
        DOCKER_IMAGE = "22127422/${params.USER_ID.toLowerCase()}-simple-webapp"
    }

    stages {
        stage('Build') {
            steps {
                echo "Building the Docker image for ${params.USER_ID.toLowerCase()}"
                script {
                    docker.build(DOCKER_IMAGE, "--build-arg WEBSITE_FILE=${params.WEBSITE_FILE} .")
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image(DOCKER_IMAGE).push("latest")
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    def allocatedPort = allocatePort(pool: 'default').port
                    
                    def containerName = "${params.USER_ID.toLowerCase()}-webapp"
                    
                    echo "Deploying container '${containerName}' to port ${allocatedPort}"

                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"
                    sh "docker run -d --name ${containerName} -p ${allocatedPort}:5000 -e WEBSITE_FILENAME=${params.WEBSITE_FILE} ${DOCKER_IMAGE}"
                }
            }
        }
    }
}