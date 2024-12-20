import requests

def extract_result(api_response):
    if "result" not in api_response:
        return "Error: 'result' not found in the response."
    result = api_response["result"]
    if isinstance(result, list) and len(result) > 0:
        for item in result:
            if item["role"] == "assistant":
                content = item["content"]
                if "\n" not in content:
                    return content.strip()
    if isinstance(result, list):
        for item in result:
            if item["role"] == "assistant":
                content = item["content"]
                topics = [line.strip() for line in content.split("\n") if line.strip()]
                return topics
    return "Error: Unable to parse response."

BASE_URL = "https://fa16-34-73-119-196.ngrok-free.app"

entity_response = requests.post(
    f"{BASE_URL}/generate_entity",
    json={"text": "یہ اردو متن ہے"}
).json()

topics_response = requests.post(
    f"{BASE_URL}/generate_topics",
    json={"text": "یہ ایک اردو پیراگراف ہے جو مختلف موضوعات پر مشتمل ہے۔"}
).json()

entity = extract_result(entity_response)
print("Extracted Entity:", entity)

topics = extract_result(topics_response)
print("Extracted Topics:", topics)
