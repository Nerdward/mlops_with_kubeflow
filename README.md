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

### API Endpoints in Tensorflow Serving
* REST is a communication “protocol” used by web applications. It defines a communication style on how clients communicate with web services. REST clients communicate with the server using the standard HTTP methods like GET, POST, DELETE, etc. The payloads of the requests are mostly encoded in JSON format.

* gRPC on the other hand is a communication protocol initially developed at Google. The standard data format used with gRPC is called the protocol buffer. gRPC provides low- latency communication and smaller payloads than REST and is preferred when working with extremely large files during inference. 


* ```bash
  docker run -it --rm -p 8501:8501 tfserving_classifier:v01
  ```
* ```python
  python predict.py
  ```
  `http://{HOST}:{PORT}/v1/models/{MODEL_NAME}:{VERB}`  
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

kubectl get svc istio-ingressgateway -n istio-system

kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80


```bash
INGRESS_HOST="localhost"
INGRESS_PORT="8080"
DOMAIN="example.com"
NAMESPACE="kserve-test"
SERVICE="sklearn-iris"

SERVICE_HOSTNAME="${SERVICE}.${NAMESPACE}.${DOMAIN}"

curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${INGRESS_HOST}:${INGRESS_PORT}/v1/models/sklearn-iris:predict -d @./iris-input.json
```

# Running tensorflow model in Kserve
Download the model
  ```bash
  wget https://github.com/alexeygrigorev/mlbookcamp-code/releases/download/chapter7-model/xception_v4_large_08_0.894.h5
  ```

Convert it to *saved_model*:
```python
python convert.py
```
Instead of using an s3 bucket or Google cloud storage
```bash
cd clothing-model/
tar -cvf artifacts.tar 1/
gzip < artifacts.tar > artifacts.tgz
```
Host the file on your local machine
```python
python -m http.server
```
```bash
kubectl apply -f tensorflow.yaml 
```
```bash
curl -v -H "Host: clothes.default.example.com" http://${INGRESS_HOST}:${INGRESS_PORT}/v1/models/clothes:predict -d $INPUT_PATH
```

## Deploy transformer with InferenceService
*Create custom image transformer* [link](https://kserve.github.io/website/master/modelserving/v1beta1/transformer/torchserve_image_transformer/#create-custom-image-transformer)

1. Create a python script with ImageTransformer Class inheriting from kserve.Model

2. Build Transformer docker image and push to dockerhub
  ```python
  docker build -t nerdward/image-transformer:v02 .
  docker build -t <hub-user>/<repo-name>[:<tag>]

  docker push nerdward/image-transformer:v02
  docker push <hub-user>/<repo-name>:<tag>
  ```

3. Create the InferenceService and Apply.
  ```bash
  kubectl apply -f transformer.yaml
  ```
4. Run a prediction.

## References and Important links
1. [How to Serve Machine Learning Models With TensorFlow Serving and Docker](https://neptune.ai/blog/how-to-serve-machine-learning-models-with-tensorflow-serving-and-docker)
2.[Machine Learning Bookcamp](https://github.com/alexeygrigorev/mlbookcamp-code)
3. [Kserve official documentation](https://kserve.github.io/website/master/)