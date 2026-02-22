from deep_translator import DeeplTranslator
import sys

api_key = "a79c6867-edb7-4699-84da-9480aa7c64a2:fx"
target = "tr"
text = "Hello world"

print(f"Testing API Key: {api_key}")

try:
    # Test 1: Standard Init with use_free_api=True
    print("\n--- Test 1: use_free_api=True ---")
    translator = DeeplTranslator(api_key=api_key, use_free_api=True)
    res = translator.translate(text, target=target)
    print(f"Success! Result: {res}")
except Exception as e:
    print(f"Test 1 Failed: {e}")

try:
    # Test 2: Standard Init with use_free_api=False
    print("\n--- Test 2: use_free_api=False ---")
    translator = DeeplTranslator(api_key=api_key, use_free_api=False)
    res = translator.translate(text, target=target)
    print(f"Success! Result: {res}")
except Exception as e:
    print(f"Test 2 Failed: {e}")

try:
    # Test 3: Standard Init default
    print("\n--- Test 3: Default ---")
    translator = DeeplTranslator(api_key=api_key)
    res = translator.translate(text, target=target)
    print(f"Success! Result: {res}")
except Exception as e:
    print(f"Test 3 Failed: {e}")
