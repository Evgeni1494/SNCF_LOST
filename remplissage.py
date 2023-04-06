import sqlite3
import pandas as pd

# Ouvrir la connexion à la base de données
conn = sqlite3.connect('SNCF_LOST.db')

# Créer un curseur
cur = conn.cursor()

# Paris Austerlitz, Paris Bercy, Paris Est, Paris Gare de Lyon, Paris Gare du Nord, Paris Montparnasse, Paris Saint-Lazare.

# Ouvrir les fichiers CSV avec pandas
df1 = pd.read_csv('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/objets2022/Paris Saint-Lazare2022.csv')
# df2 = pd.read_csv('fichier2.csv')
# df3 = pd.read_csv('fichier3.csv')
# df4 = pd.read_csv('fichier4.csv')

# Définir les valeurs pour GarePerte et AnneePerte
gare_perte = "Paris Saint-Lazare"
annee_perte = "2022"

# Parcourir les DataFrames et insérer les données dans la table ObjetPerdu
for df in [df1]:
    for index, row in df.iterrows():
        type_objet = row['fields.gc_obo_nature_c']
        date = row['fields.date']
        gare_perte = gare_perte
        annee_perte = annee_perte
        # Exécuter la requête SQL INSERT
        cur.execute("INSERT INTO ObjetPerdu (id, TypeObjet, Date, GarePerte, AnneePerte) VALUES (NULL, ?, ?, ?, ?)", ( type_objet, date, gare_perte, annee_perte))

# Valider les modifications et fermer la connexion à la base de données
conn.commit()
cur.close()
conn.close()
