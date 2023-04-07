import os
import pandas as pd

# Le chemin d'accès des dossiers contenant les fichiers CSV
folders_path = ["/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/objets2019", 
                "/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/objets2020", 
                "/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/objets2021", 
                "/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/objets2022"]

# Liste pour stocker les dataframes de chaque fichier CSV
dataframes = []

# Parcourir chaque dossier et ajouter les dataframes de chaque fichier CSV à la liste
for folder in folders_path:
    csv_files = os.listdir(folder)
    for csv_file in csv_files:
        # Vérifier que le fichier est bien un fichier CSV
        if csv_file.endswith(".csv"):
            file_path = os.path.join(folder, csv_file)
            df = pd.read_csv(file_path)
            dataframes.append(df)

# Fusionner les dataframes en un seul dataframe
merged_df = pd.concat(dataframes, ignore_index=True)

# Enregistrer le dataframe fusionné dans un fichier CSV
merged_df.to_csv("Data_SNCF_LOST_2019_2022.csv", index=False)
