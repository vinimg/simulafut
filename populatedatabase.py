// 




api = 'https://api.football-data.org/v4/competitions/BSA/matches'

import requests
import json
import sqlite3


def populate_database():
    response = requests.get(api, headers={'X-Auth-Token': '8157a18ac06244cfae16a3d016a78080'})
    data = response.json()
    matches = data['matches']
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM simuladorbrabo_team')
    

https://api.football-data.org/v4/matches