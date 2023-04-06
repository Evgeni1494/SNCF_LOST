import sqlite3
import pandas as pd


conn = sqlite3.connect('ma_base_de_donnees.db')
c = conn.cursor()

# création de la table Objet
c.execute('''CREATE TABLE Objet
             (id INTEGER PRIMARY KEY,
             TypeObjet TEXT,
             Date TEXT,
             GareStatus TEXT)''')

# création de la table Gare
c.execute('''CREATE TABLE Gare
             (id INTEGER PRIMARY KEY,
             Nom TEXT,
             Position TEXT,
             Frequentation INTEGER)''')

# création de la table Temperature
c.execute('''CREATE TABLE Temperature
             (id INTEGER PRIMARY KEY,
             Date TEXT,
             TempMed REAL)''')

conn.commit()
conn.close()



# lecture du fichier CSV
df = pd.read_csv('mon_fichier.csv')

# ouverture de la connexion à la base de données
conn = sqlite3.connect('ma_base_de_donnees.db')
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
