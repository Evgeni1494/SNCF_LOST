import sqlite3
import pandas as pd


conn = sqlite3.connect('SNCF_LOST.db')
c = conn.cursor()

# création de la table Objet
c.execute('''DELETE FROM ObjetPerdu WHERE AnneePerte = 2021;
''')

conn.commit()
conn.close()