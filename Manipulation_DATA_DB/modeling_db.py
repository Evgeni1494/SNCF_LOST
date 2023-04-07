import sqlite3
import pandas as pd


conn = sqlite3.connect('SNCF_LOST.db')
c = conn.cursor()

# création de la table Objet
c.execute('''CREATE TABLE IF NOT EXISTS ObjetPerdu
             (id INTEGER PRIMARY KEY,
             TypeObjet TEXT,
             Date TEXT,
             Status TEXT)''')

# création de la table Gare
c.execute('''CREATE TABLE IF NOT EXISTS Gare
             (id INTEGER PRIMARY KEY,
             Nom TEXT,
             Position TEXT,
             Frequentation INTEGER)''')

# création de la table Temperature
c.execute('''CREATE TABLE IF NOT EXISTS Temperature
             (id INTEGER PRIMARY KEY,
             Date TEXT,
             TempMed REAL)''')

conn.commit()
conn.close()




