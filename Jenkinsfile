pipeline {
    agent any

    environment {
        IMAGE_NAME = "devops-poc:latest"
        CLUSTER_NAME = "devops-lab"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/<your-username>/devops-poc.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Push to kind Cluster') {
            steps {
                sh 'kind load docker-image $IMAGE_NAME --name $CLUSTER_NAME'
            }
        }
    }
}

