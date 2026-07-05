import requests
import os

api_key = os.environ.get("OPENAI_API_KEY", "")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "hi"}]
}
res = requests.post("https://api.openai-proxy.org/v1/chat/completions", headers=headers, json=data)
print(res.status_code)
print(res.text)