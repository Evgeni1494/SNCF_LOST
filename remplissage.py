import sqlite3
import pandas as pd



# lecture du fichier CSV
df = pd.read_csv('mon_fichier.csv')

# ouverture de la connexion à la base de données
conn = sqlite3.connect('SNCF_LOST.db')
c = conn.cursor()

# boucle sur chaque ligne du DataFrame
for index, row in df.iterrows():
    TypeObjet = row['fields.gc_obo_nom_recordtype_sc_c']
    Date = row['fields.date']
    GareStatus = row['fields.gc_obo_gare_origine_r_name']

    # insertion de la ligne dans la table Objet
    c.execute("INSERT INTO Objet (TypeObjet, Date, GareStatus) VALUES (?, ?, ?)", (TypeObjet, Date, GareStatus))

# validation de la transaction et fermeture de la connexion à la base de données
conn.commit()
conn.close()