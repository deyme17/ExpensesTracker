import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("MONOBANK_TOKEN")

def get_client_info(token):
    url = "https://api.monobank.ua/personal/client-info"
    headers = {"X-Token": token}

    response = requests.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Error:", response.text)
        return

    data = response.json()
    print("\n[DEBUG] Відповідь від Monobank API:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    accounts = data.get("accounts", [])
    print(f"\nРахунки: {len(accounts)}")
    for i, acc in enumerate(accounts, 1):
        print(f"  #{i}: Balance: {acc.get('balance', 0)/100:.2f} грн, Currency: {acc.get('currencyCode')}, Type: {acc.get('type')}")

if __name__ == "__main__":
    if TOKEN:
        get_client_info(TOKEN)
    else:
        print("Токен не знайдено")
