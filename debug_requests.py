import requests

api_key = "a79c6867-edb7-4699-84da-9480aa7c64a2:fx"
url = "https://api-free.deepl.com/v2/translate"
params = {
    "auth_key": api_key,
    "text": "Hello world",
    "target_lang": "TR"
}

print(f"Testing direct request to {url}...")
try:
    resp = requests.post(url, data=params)
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Request failed: {e}")
