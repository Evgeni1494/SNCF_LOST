import sqlite3
import pandas as pd

# Se connecter à la base de données SQLite
conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')
c = conn.cursor()

# Lire le fichier CSV et créer un DataFrame Pandas en nommant les colonnes
df = pd.read_csv('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/Temperature/temp_paris.csv', header=0, names=['Date', 'TempMed'])

# Écrire les données du DataFrame dans la table SQLite en créant les colonnes
df.to_sql('Temperature', conn, if_exists='replace', index=False,
          dtype={'Date': 'TEXT', 'TempMed': 'INTEGER'})

# Confirmer les modifications en enregistrant les modifications
conn.commit()

# Fermer la connexion à la base de données
conn.close()



