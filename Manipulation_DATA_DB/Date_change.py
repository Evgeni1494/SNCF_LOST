import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')

# Ouverture d'un curseur
cur = conn.cursor()

# Requête SQL pour mettre à jour la colonne date_col
sql_query = "UPDATE ObjetPerdu SET Date = strftime('%Y-%m-%d', Date)"

# Exécution de la requête SQL
cur.execute(sql_query)

# Validation de la transaction
conn.commit()

# Fermeture du curseur et de la connexion
cur.close()
conn.close()



import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')
cur = conn.cursor()

# Ajout des colonnes Latitude et Longitude à la table ObjetPerdu
cur.execute("ALTER TABLE Gare ADD COLUMN Latitude FLOAT")
cur.execute("ALTER TABLE Gare ADD COLUMN Longitude FLOAT")

# Mise à jour des valeurs de Latitude et Longitude à partir de la colonne Position
cur.execute("UPDATE Gare SET Latitude = substr(Position, 2, instr(Position, ',')-2), \
             Longitude = substr(Position, instr(Position, ',')+1, length(Position)-instr(Position, ',')-1)")

# Enregistrement des modifications et fermeture de la connexion à la base de données
conn.commit()
conn.close()
