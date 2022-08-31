# Tf-serving
## Setup 
1. Install [Kind (Kubernetes in Docker)](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
   I am using kind here in place of minikube because it will enable me install kserve as a standalone.

2. Install [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Steps
*It is required that you have Anaconda(python) and tensorflow installed.*
* ```python
  python model.py
  ```
  *To train the model and save it in SavedModel format for the tensorflow serving service.*

* ```bash
  docker build -t tfserving_classifier:v01 .
  ```

* ```bash
  docker run -it --rm -p 8501:8501 tfserving_classifier:v01
  ```
* ```python
  python predict.py
  ```
*To load images from your local into the cluster*
* ```bash
  kind load docker-image tfserving_classifier:v01
  ```
* ```bash
  kubectl apply -f kubeconfig/deployment.yaml
  ```
* ```bash
  kubectl apply -f kubeconfig/service.yaml
  ```

# Kserve
## Setup
1. Install [Kserve](https://kserve.github.io/website/master/get_started/)  standalone (requires kind and kubectl)

2. Run your first [InferenceService](https://kserve.github.io/website/master/get_started/first_isvc/)
