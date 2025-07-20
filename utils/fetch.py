import os
import requests
from dotenv import load_dotenv

load_dotenv()

XANO_API_URL = os.environ.get("XANO_API_URL")

def fetch_categories(email, userToken):
    headers = {
        "Authorization": 'Bearer ' + userToken,
        "Content-Type": "application/json"
    }
    payload = {"user_input": email}

    response = requests.post(XANO_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
