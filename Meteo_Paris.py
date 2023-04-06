import requests
import sqlite3
from datetime import datetime, timedelta

# clé API OpenWeatherMap
api_key = "a30f2215f9805d9d0a26c9183cf9b58d"

# ville de Paris
city = "Paris"

# date de début de la période
start_date = datetime(2022, 1, 1)

# date de fin de la période
end_date = datetime(2022, 12, 31)

# ouverture de la connexion à la base de données
conn = sqlite3.connect('SNCF_LOST.db')
c = conn.cursor()

# création de la table Temperature
c.execute('''CREATE TABLE IF NOT EXISTS Temperature
             (id INTEGER PRIMARY KEY,
             Date TEXT,
             TempMed REAL)''')

# boucle sur chaque jour de la période
current_date = start_date
while current_date <= end_date:
    # requête de l'API OpenWeatherMap pour récupérer les données météorologiques du jour
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&dt={int(current_date.timestamp())}"
    response = requests.get(url)

    if response.status_code == 200:
        # extraction de la température moyenne de la réponse JSON
        data = response.json()
        temp_med = data["main"]["temp"]

        # insertion de la température moyenne dans la table Temperature
        date_str = current_date.strftime('%Y-%m-%d')
        c.execute("INSERT INTO Temperature (Date, TempMed) VALUES (?, ?)", (date_str, temp_med))
    else:
        print(f"La requête a échoué avec le code de statut {response.status_code}.")

    # passage au jour suivant
    current_date += timedelta(days=1)

# validation de la transaction et fermeture de la connexion à la base de données
conn.commit()
conn.close()
