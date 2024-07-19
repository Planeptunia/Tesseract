import requests
import json
import libs.TesseractFuncs as Funcs
import libs.Types.TesseractTypes as Types

env = Funcs.get_dotenv()

QUAVER_API_DOMAIN = env["QUAVER_API_DOMAIN"]
QUAVER_APIv2_DOMAIN = env['QUAVER_APIv2_DOMAIN']

def search_by_name(username: str) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/search/{username}")
    return json.loads(resp.content)

def get_profile_by_id_or_name(id: str | int) -> Types.QuaverUser:
    resp = requests.get(f"{QUAVER_APIv2_DOMAIN}/user/{id}")
    response = Types.QuaverAPIResponse(resp.status_code, json.loads(resp.content))
    return Types.QuaverUser(response.content['user'])
    
def search_by_namev2(username: str) -> list[Types.QuaverUser]:
    resp = requests.get(f"{QUAVER_APIv2_DOMAIN}/user/search/{username}")
    response = Types.QuaverAPIResponse(resp.status_code, json.loads(resp.content))
    user_list = []
    for user in response.content['users']:
        new_user = Types.QuaverUser(user)
        user_list.append(new_user)
    return user_list

def get_achievements_by_idv2(id: int) -> list[Types.QuaverAchievement]:
    resp = requests.get(f"{QUAVER_APIv2_DOMAIN}/user/{id}/achievements")
    response = Types.QuaverAPIResponse(resp.status_code, json.loads(resp.content))
    achievement_list = []
    for achievement in response.content['achievements']:
        new_achievement = Types.QuaverAchievement(achievement)
        achievement_list.append(new_achievement)
    return achievement_list

def get_mini_profile_by_id(id: int) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users", params={'id': id})
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

def get_recent_scores_by_id(id: int, mode: int = 1, limit: int = 50) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/users/scores/recent", params={"id": id, "mode": mode, "limit": limit})
    return json.loads(resp.content)

def get_map_info_by_id(id: int) -> dict:
    resp = requests.get(f"{QUAVER_API_DOMAIN}/maps/{id}")
    return json.loads(resp.content)