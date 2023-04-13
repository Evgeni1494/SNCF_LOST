import requests
import pandas as pd

# Liste des gares de Paris à cibler
gares = ["Paris Austerlitz", "Paris Bercy", "Paris Est", "Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", "Paris Saint-Lazare"]

# Parcourir la liste des gares de Paris et récupérer les données des objets trouvés pour chaque gare
for gare in gares:
    url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q={gare}&lang=fr&rows=10000&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data["records"])
        # Enregistrer les données dans un fichier CSV avec le nom de la gare
        filename = f"{gare}2022.csv"
        df.to_csv(filename, index=False)
    else:
        print(f"La requête pour la gare {gare} a échoué avec le code de statut :", response.status_code)
