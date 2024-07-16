import requests
import json
import libs.TesseractFuncs as Funcs

env = Funcs.get_dotenv()

QUAVER_API_DOMAIN = env["QUAVER_API_DOMAIN"]

def search_by_name(username: str) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/search/{username}")
    return json.loads(resp.content)

def get_full_profile_by_id(id: int) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/full/{id}")
    return json.loads(resp.content)

def get_achievements_by_id(id: int) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/{id}/achievements")
    return json.loads(resp.content)

def get_best_scores_by_id(id: int, mode: int = 1, limit: int = 50) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/scores/best", params={"id": id, "mode": mode, "limit": limit})
    return json.loads(resp.content)