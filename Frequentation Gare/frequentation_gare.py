import requests
import pandas as pd

# Définir l'URL de l'API
url = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=frequentation-gares&q=paris&rows=100&sort=nom_gare&facet=nom_gare&facet=code_postal&facet=segmentation_drg"

# Récupérer les données à partir de l'API
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    print("La requête a réussi !")
else:
    print("La requête a échoué.")

# Convertir la réponse en un objet json
data = response.json()

# Créer un DataFrame à partir de l'objet json
df = pd.DataFrame.from_dict(data["records"])
df = pd.json_normalize(data["records"])
# Enregistrer les données dans un fichier CSV
df.to_csv("Position_gare.csv", index=False)

print("Les données ont été enregistrées dans le fichier 'donnees_gares.csv'")



