import requests
import os

XANO_ENDPOINT = os.getenv("XANO_ENDPOINT")

def fetch_categories(email, userToken):
    headers = {
        "Authorization": "Bearer " + userToken,
        "Content-Type": "application/json"
    }
    payload = {
        "user_input": email
    }

    response = requests.post(XANO_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return {k: v for k, v in data.items() if k.startswith("dim")}
