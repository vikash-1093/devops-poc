pipeline {
  agent { label 'docker-kind' }   // change/remove per your setup
  environment {
    IMAGE_REPO  = "devops-poc"
    CLUSTER_NAME = "devops-lab"
    GIT_CRED_ID = "github-app-password" // Jenkins credential ID for PAT
  }

  stages {
    stage('Checkout') {
      steps {
        // Use credentialsId to fetch over HTTPS using stored PAT
        git url: 'https://github.com/vikash-1093/devops-poc.git',
            branch: 'main',
            credentialsId: env.GIT_CRED_ID
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          set -eux
          # tag with short commit SHA for traceability
          SHA=$(git rev-parse --short HEAD)
          IMAGE="${IMAGE_REPO}:${SHA}"
          echo "Building ${IMAGE}"
          docker build -t "${IMAGE}" .
          # also tag :latest if you want
          docker tag "${IMAGE}" "${IMAGE_REPO}:latest" || true
          echo "${IMAGE}" > .built_image
        '''
      }
    }

    stage('Load into kind') {
      steps {
        sh '''
          set -eux
          IMAGE=$(cat .built_image)
          # ensure kind cluster exists on this node
          if ! kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
            echo "Kind cluster ${CLUSTER_NAME} not found on this agent"
            exit 1
          fi
          kind load docker-image "${IMAGE}" --name "${CLUSTER_NAME}"
        '''
      }
    }
  }

  post {
    always {
      echo "Pipeline finished"
    }
  }
}
