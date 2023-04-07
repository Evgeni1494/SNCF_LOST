import sqlite3
import pandas as pd


conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')
c = conn.cursor()

# création de la table Objet
c.execute('''DROP TABLE NomDeLaTable;
''')

conn.commit()
conn.close()