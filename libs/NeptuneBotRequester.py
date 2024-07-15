import requests
from bs4 import BeautifulSoup
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

def get_grades_by_id(id: int):
    amounts = {"X": 0, "SS": 0, "S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
    for grade in amounts.keys():
        grade_amount = amounts[grade]
        page = 0
        while True:
            resp = requests.get(f"{QUAVER_API_DOMAIN}/users/scores/grades", params={'mode': 1, 'id': id, 'grade': grade, "page": page}, headers={'Content-Type': "application/json"})
            grade_resp_amount = len(json.loads(resp.content)['scores'])
            if grade_resp_amount > 0:
                grade_amount += grade_resp_amount
                page += 1
            else:
                break
            
        amounts[grade] = grade_amount
    return amounts
        