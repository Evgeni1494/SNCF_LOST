import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')

# Chargement des données dans un DataFrame pandas
df = pd.read_sql_query("SELECT * FROM Gare;", conn)

# Suppression des deux colonnes
df = df.drop(columns=['Position'])

# Mise à jour de la table Gare dans la base de données
df.to_sql('Gare', conn, if_exists='replace', index=False)

# Fermeture de la connexion à la base de données
conn.close()
