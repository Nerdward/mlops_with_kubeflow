## Before you get started
* You should be familiar with Kubernetes, Kubectl and kustomize
* For native support of kustomize, you will need kubectl v1.14 or higher. You can download and install kubectl by following the kubectl installation guide.

## Setup a local Kubernetes cluster using:
* Minikube
* kind *(Preferable)*
* K3s

## Deploying Kubeflow Pipelines
The installation process for Kubeflow Pipelines is the same for any environments above.
1. To deploy the Kubeflow Pipelines, run the following commands:
    ```bash
    # env/platform-agnostic-pns hasn't been publically released, so you will install it from master
    export PIPELINE_VERSION=2.0.3
    kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
    kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
    kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
    ```

    The Kubeflow Pipelines deployment may take several minutes to complete

2. Verify the Kubeflow Pipelines UI is accessible by port-forwading:
    ```bash
    kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
    ```

    Then, open the Kubeflow Pipelines UI at *http://localhost:8080/* or - if you are using kind or K3s within a virtual machine - *http://{YOUR_VM_IP_ADDRESS}:8080/*



