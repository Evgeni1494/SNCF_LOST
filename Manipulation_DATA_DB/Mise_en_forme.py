import pandas as pd

# Charger le fichier CSV en tant que DataFrame
df = pd.read_csv("/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/Position_Gare.csv")

# Filtrer les données pour garder uniquement les lignes avec la valeur "ETAB GARES PARIS" dans la colonne fields.gare_nbpltf
df_filtered = df[df["fields.gare_agencegc_libelle"] == "ETAB GARES PARIS"]

# Enregistrer les données filtrées dans un nouveau fichier CSV
df_filtered.to_csv("Position_Gare_New.csv", index=False)

print("Les données ont été filtrées et enregistrées dans le fichier 'nom_du_fichier_filtre.csv'")
