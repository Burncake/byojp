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
                    // --- THE RELIABLE PORT ALLOCATION LOGIC ---
                    // 1. Define the base port and range
                    def basePort = 50000
                    def portRange = 1000
                    // 2. Generate a unique, consistent port from the user's ID
                    def allocatedPort = basePort + (Math.abs(params.USER_ID.toLowerCase().hashCode()) % portRange)
                    
                    def containerName = "${params.USER_ID.toLowerCase()}-webapp"
                    
                    echo "Deploying container '${containerName}' to generated port ${allocatedPort}"

                    // 3. Use the generated port to run the container
                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"
                    sh "docker run -d --name ${containerName} -p ${allocatedPort}:5000 -e WEBSITE_FILENAME=${params.WEBSITE_FILE} ${DOCKER_IMAGE}"
                }
            }
        }
    }
}