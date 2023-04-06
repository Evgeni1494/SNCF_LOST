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

conn.commit()
conn.close()