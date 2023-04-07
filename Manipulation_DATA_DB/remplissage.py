# import sqlite3
# import pandas as pd

# # Ouvrir la connexion à la base de données
# conn = sqlite3.connect('SNCF_LOST.db')

# # Créer un curseur
# cur = conn.cursor()

# # Paris Austerlitz, Paris Bercy, Paris Est, Paris Gare de Lyon, Paris Gare du Nord, Paris Montparnasse, Paris Saint-Lazare.

# # Ouvrir les fichiers CSV avec pandas
# df1 = pd.read_csv('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/objets2022/Paris Saint-Lazare2022.csv')
# # df2 = pd.read_csv('fichier2.csv')
# # df3 = pd.read_csv('fichier3.csv')
# # df4 = pd.read_csv('fichier4.csv')

# # Définir les valeurs pour GarePerte et AnneePerte
# gare_perte = "Paris Saint-Lazare"
# annee_perte = "2022"

# # Parcourir les DataFrames et insérer les données dans la table ObjetPerdu
# for df in [df1]:
#     for index, row in df.iterrows():
#         type_objet = row['fields.gc_obo_nature_c']
#         date = row['fields.date']
#         gare_perte = gare_perte
#         annee_perte = annee_perte
#         # Exécuter la requête SQL INSERT
#         cur.execute("INSERT INTO ObjetPerdu (id, TypeObjet, Date, GarePerte, AnneePerte) VALUES (NULL, ?, ?, ?, ?)", ( type_objet, date, gare_perte, annee_perte))

# # Valider les modifications et fermer la connexion à la base de données
# conn.commit()
# cur.close()
# conn.close()





# import pandas as pd
# import sqlite3

# # Connexion à la base de données
# conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')

# # Lecture des données du fichier CSV avec pandas
# df = pd.read_csv('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/Frequentation Gare/Frequentation_gare.csv')

# # Création d'un nouveau DataFrame avec les colonnes souhaitées
# new_df = df[['fields.nom_gare', 'fields.total_voyageurs_non_voyageurs_2019', 'fields.total_voyageurs_non_voyageurs_2020', 'fields.total_voyageurs_non_voyageurs_2021']].copy()

# # Renommage des colonnes pour correspondre à la structure de la table
# new_df.columns = ['nom', 'Freq_2019', 'Freq_2020', 'Freq_2021']

# # Ajout des données manquantes dans la colonne Freq_2022
# new_df['Freq_2022'] = new_df['Freq_2021']

# # Écriture des données dans la table de la base de données
# new_df.to_sql('Gare', conn, if_exists='append', index=False)

# # Fermeture de la connexion à la base de données
# conn.close()




# import sqlite3
# import pandas as pd

# # Connexion à la base de données
# conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')
# c = conn.cursor()

# # Chargement des données depuis le fichier CSV
# df = pd.read_csv('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/Position Gare/Position_Gare_New.csv')

# # Ajout de la position des gares dans la colonne "Position"
# for i, row in df.iterrows():
#     nom_gare = row['fields.gare_alias_libelle_noncontraint']
#     position = row['fields.wgs_84']
#     c.execute('UPDATE Gare SET Position = ? WHERE Nom = ?', (position, nom_gare))
    
# # Enregistrement des modifications et fermeture de la connexion
# conn.commit()
# conn.close()
