import requests
import dotenv
import os
import json



QUAVER_API_DOMAIN = os.getenv("QUAVER_API_DOMAIN")

def search_by_name(username: str) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/search/{username}")
    return json.loads(resp.content)

def get_full_profile_by_id(id: int) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/full/{id}")
    return json.loads(resp.content)

def get_achievements_by_id(id: int) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/{id}/achievements")
    return json.loads(resp.content)