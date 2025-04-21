import requests
import uuid
import re
uuid = uuid.uuid1()
import json
import random
import string

def generate_custom_uuid(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

uuid_custom = generate_custom_uuid()


url = "https://id.vk.com/auth"
params = {
    "response_type": "silent_token",
    "uuid": uuid_custom,           # Сгенерируйте UUID
    "v": "1.0.2",
    "app_id": "7497650",          # Замените на ID вашего приложения
    "redirect_uri": "https://id.vk.com/account?flow_service=vkid_landing_/id"
}
url1 = "https://id.vk.com/auth?response_type=silent_token"
response = requests.post(url1)


headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://id.vk.com/"
}

response = requests.get(url, params=params, cookies=response.cookies, headers=headers)

print(response.status_code)
print(response.text)

auth_pattern = re.compile(r'"auth":\s*{.*?}', re.DOTALL)
match = auth_pattern.search(response.text)

if match:
    print("Found 'auth' block:")
    print(match.group(0)[7:])
    print(match)
else:
    print("Block 'auth' not found.")

# Извлечение блока auth
auth_data = json.loads(match.group(0)[7:])

# Вывод всех ключей и значений
for key, value in auth_data.items():
    print(f"{key}: {value}")