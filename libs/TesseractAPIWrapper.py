import requests
import json
import libs.TesseractFuncs as Funcs
import libs.Types.TesseractTypes as Types
from libs.Types.TesseractTypes import tesseract_logger as Logger

env = Funcs.get_dotenv()
QUAVER_APIv2_DOMAIN = env['QUAVER_APIv2_DOMAIN']

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

def get_recent_scores_by_idv2(id: int, mode: int, page: int = 0) -> list[Types.QuaverScore]:
    resp = requests.get(f"{QUAVER_APIv2_DOMAIN}/user/{id}/scores/{mode}/recent", params={'page': page})
    response = Types.QuaverAPIResponse(resp.status_code, json.loads(resp.content))
    score_list = []
    for score in response.content['scores']:
        new_score = Types.QuaverScore(score)
        score_list.append(new_score)
    return score_list

def get_mapset_info_by_id(id: int) -> Types.QuaverMapset:
    resp = requests.get(f"{QUAVER_APIv2_DOMAIN}/mapset/{id}")
    response = Types.QuaverAPIResponse(resp.status_code, json.loads(resp.content))
    return Types.QuaverMapset(response.content['mapset'])

def get_map_info_by_id(id: int) -> Types.QuaverMapInfo:
    resp = requests.get(f"{QUAVER_APIv2_DOMAIN}/map/{id}")
    response = Types.QuaverAPIResponse(resp.status_code, json.loads(resp.content))
    return Types.QuaverMapInfo(response.content['map'])

def get_user_pb_by_md5(map_md5: str, user_id: int) -> Types.QuaverScore:
    resp = requests.get(f"{QUAVER_APIv2_DOMAIN}/scores/{map_md5}/{user_id}/all")
    response = Types.QuaverAPIResponse(resp.status_code, json.loads(resp.content))
    return Types.QuaverScore(response.content['score'])    
