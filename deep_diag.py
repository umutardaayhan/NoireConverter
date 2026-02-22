import requests
import json

API_KEY = "a79c6867-edb7-4699-84da-9480aa7c64a2:fx"

print(f"--- DeepL API Diagnostic Tool ---")
print(f"Key: {API_KEY}")

def test_endpoint(url, name):
    print(f"\nTesting {name} ({url})...")
    try:
        # Just checking usage is a good way to validate key without translating
        usage_url = url.replace("/translate", "/usage")
        headers = {"Authorization": f"DeepL-Auth-Key {API_KEY}"}
        
        print(f"  > GET {usage_url}")
        resp = requests.get(usage_url, headers=headers)
        
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.text}")
        
        if resp.status_code == 200:
            print("  [SUCCESS] Key is valid and working on this endpoint.")
            return True
        elif resp.status_code == 403:
            print("  [FAILURE] 403 Forbidden. Key is rejected by this endpoint.")
        elif resp.status_code == 401:
            print("  [FAILURE] 401 Unauthorized. Key is wrong.")
        else:
            print(f"  [FAILURE] Unexpected error.")
            
    except Exception as e:
        print(f"  [Error] Connection failed: {e}")
    return False

# Test Free API
free_ok = test_endpoint("https://api-free.deepl.com/v2/translate", "FREE API")

# Test Pro API (just in case)
pro_ok = test_endpoint("https://api.deepl.com/v2/translate", "PRO API")

if not free_ok and not pro_ok:
    print("\n[CONCLUSION] The API Key appears to be invalid or blocked on BOTH endpoints.")
    print("Please check your DeepL account status.")
elif free_ok:
    print("\n[CONCLUSION] The API Key is valid for FREE API.")
elif pro_ok:
    print("\n[CONCLUSION] The API Key is valid for PRO API.")
