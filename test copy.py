import folium
import pandas as pd
import sqlite3
import streamlit as st
from streamlit_folium import folium_static


# Connexion à la base de données
conn = sqlite3.connect('SNCF_LOST.db')

# Récupération des données depuis la base de données
query = "SELECT o.TypeObjet, o.Date, o.GarePerte, o.AnneePerte, g.Nom, g.Freq_2019, g.Freq_2020, g.Freq_2021, g.Freq_2022, g.Latitude, g.Longitude \
         FROM ObjetPerdu o \
         INNER JOIN Gare g ON o.GarePerte = g.Nom"
df = pd.read_sql_query(query, conn)

# Création d'une carte centrée sur Paris
paris_coords = [48.8566, 2.3522]
m = folium.Map(location=paris_coords, zoom_start=12)

# Choix de l'année et du type d'objet à afficher
year = st.sidebar.selectbox("Année", ['2019', '2020', '2021', '2022'])
obj_type = st.sidebar.selectbox("Type d'objet", df.TypeObjet.unique())

# Filtrage des données en fonction de l'année et du type d'objet choisi
df_filtered = df[(df.AnneePerte == year) & (df.TypeObjet == obj_type)]

# Calcul du nombre d'objets trouvés par gare en fonction de l'année.
df_filtered.loc[:,'NbObjets'] = df_filtered.apply(lambda row: row['Freq_'+year] * 0.01, axis=1)

# Création des marqueurs sur la carte
for index, row in df_filtered.iterrows():
    popup_text = "Gare : " + row['Nom'] + "<br>" + "Fréquentation " + year + " : " + str(row['Freq_'+year]) + "<br>" + "Nombre d'objets trouvés : " + str(row['NbObjets'])
    folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup_text).add_to(m)

# Affichage de la carte sur Streamlit
st.title("Carte des objets perdus dans les gares de Paris")
st.sidebar.title("Paramètres")
st.sidebar.write("Année choisie :", year)
st.sidebar.write("Type d'objet choisi :", obj_type)
folium_static(m)