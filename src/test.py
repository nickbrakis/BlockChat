import requests
import json

url = "http://127.0.0.1:8002/receive_mapping"  # Replace with your actual API endpoint URL

try:
    mapping = {
        1: ("public_key1", "ip1", "8001"),
        2: ("public_key2", "ip2", "8002"),
        3: ("public_key3", "ip3", "8003"),
    }
except requests.exceptions.RequestException as e:
    print("Error:", e)

response = requests.post(url, json=mapping)

print(response.status_code)
print(response.text)