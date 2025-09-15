pipeline {
  //agent { label 'docker-kind' }
  agent any
  environment {
    IMAGE_REPO    = "devops-poc"
    CLUSTER_NAME  = "devops-lab"
    GIT_CRED_ID   = "github-app-password" // ensure this exists in Jenkins
    K8S_NAMESPACE = "default"
    DEPLOYMENT    = "devops-poc"
    BUILD_TIMEOUT = 30  // minutes
  }

  options {
    timeout(time: env.BUILD_TIMEOUT as Integer, unit: 'MINUTES')
    ansiColor('xterm')
  }

  stages {
    stage('Prep / Diagnostics') {
      steps {
        sh '''
          set -eux
          echo "=== Tool versions ==="
          docker --version || true
          kind --version || true
          kubectl version --client || true
          echo "=== Check kind cluster ==="
          kind get clusters || true
        '''
      }
    }

    stage('Checkout') {
      steps {
        git url: 'https://github.com/vikash-1093/devops-poc.git',
            branch: 'main',
            credentialsId: env.GIT_CRED_ID
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          set -eux
          SHA=$(git rev-parse --short HEAD)
          IMAGE="${IMAGE_REPO}:${SHA}"
          echo "Building ${IMAGE}"
          docker build -t "${IMAGE}" .
          docker tag "${IMAGE}" "${IMAGE_REPO}:latest" || true
          echo "${IMAGE}" > .built_image
        '''
      }
    }

    stage('Validate cluster & Load image') {
      steps {
        sh '''
          set -eux
          IMAGE=$(cat .built_image)
          if ! kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
            echo "ERROR: kind cluster ${CLUSTER_NAME} not found on this node"
            echo "Run: kind create cluster --name ${CLUSTER_NAME}"
            exit 2
          fi
          kind load docker-image "${IMAGE}" --name "${CLUSTER_NAME}"
        '''
      }
    }

    stage('Restart k8s deployment') {
      steps {
        sh '''
          set -eux
          kubectl -n ${K8S_NAMESPACE} rollout restart deployment/${DEPLOYMENT} || true
          kubectl -n ${K8S_NAMESPACE} rollout status deployment/${DEPLOYMENT} --timeout=120s || true
          kubectl -n ${K8S_NAMESPACE} get pods -l app=${DEPLOYMENT} -o wide || true
        '''
      }
    }
  }

  post {
    success { echo "SUCCESS: Pipeline finished." }
    failure { echo "FAILED: Check console output for errors." }
    always { sh 'docker image prune -f || true' }
  }
}
