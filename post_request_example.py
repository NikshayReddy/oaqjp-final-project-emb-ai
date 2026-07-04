import json
import requests

url = "http://127.0.0.1:5000/detect"
payload = {"text": "I am excited and happy!"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print("Status code:", response.status_code)
print("Response body:", response.json())
