import requests


INGRESS_HOST="localhost"
INGRESS_PORT="8080"

DOMAIN="example.com"
NAMESPACE="kserve-test"
SERVICE="sklearn-iris"

SERVICE_HOSTNAME=f"{SERVICE}.{NAMESPACE}.{DOMAIN}"

url = f"http://{INGRESS_HOST}:{INGRESS_PORT}/v1/models/sklearn-iris:predict"
headers = {"Host": SERVICE_HOSTNAME}

data = {
    "instances": [
      [6.8,  2.8,  4.8,  1.4],
      [6.0,  3.4,  4.5,  1.6]
    ]
  }
response = requests.post(url, json=data, headers=headers)
print(response.json())