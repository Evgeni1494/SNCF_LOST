import folium
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
#from datetime import datetime, timedelta

# Se connecter à la base de données
conn = sqlite3.connect('SNCF_LOST.db')

# Récupérer la liste des types d'objets disponibles dans la table "ObjetPerdu"
types_objets = pd.read_sql_query("SELECT DISTINCT TypeObjet FROM ObjetPerdu", conn)['TypeObjet'].tolist()

# Afficher une liste déroulante pour sélectionner les types d'objets à inclure dans l'histogramme
selected_types = st.multiselect("Sélectionnez les types d'objets à inclure dans l'histogramme", types_objets)

# Calculer la somme des objets trouvés par semaine entre 2019 et 2022
df_objets = pd.read_sql_query("SELECT Date, TypeObjet, COUNT(*) AS NbObjets FROM ObjetPerdu WHERE AnneePerte BETWEEN 2019 AND 2022 GROUP BY Date, TypeObjet", conn)
df_objets['Date'] = pd.to_datetime(df_objets['Date'])
df_objets = df_objets.groupby([pd.Grouper(key='Date', freq='W-MON'), 'TypeObjet']).sum().reset_index()
df_objets['Semaine'] = df_objets['Date'].dt.strftime('%Y-%m-%d')

# Filtrer les données en fonction des types d'objets sélectionnés
if selected_types:
    df_objets = df_objets[df_objets['TypeObjet'].isin(selected_types)]

# Afficher l'histogramme avec Plotly
fig = px.histogram(df_objets, x='Semaine', y='NbObjets', color='TypeObjet', nbins=len(df_objets['Semaine'].unique()), labels={'Semaine': 'Semaine (année-mois-jour)', 'NbObjets': 'Nombre d\'objets trouvés'})
fig.update_layout(title="Répartition du nombre d'objets trouvés par semaine entre 2019 et 2022")
st.plotly_chart(fig)


# # Connexion à la base de données
# conn = sqlite3.connect('SNCF_LOST.db')
# cur = conn.cursor()

# Requête SQL pour récupérer le nombre d'objets trouvés par semaine
query = """
SELECT strftime('%Y-%W', Date) AS Semaine, COUNT(*) AS NbObjets
FROM ObjetPerdu
WHERE AnneePerte >= 2019 AND AnneePerte <= 2022
GROUP BY Semaine
"""

# Récupération des données dans un DataFrame pandas
df = pd.read_sql_query(query, conn)

# Création du graphique avec Plotly
fig = px.histogram(df, x="Semaine", y="NbObjets", nbins=len(df), width=1000, height=500)

# Affichage du graphique avec Streamlit
st.plotly_chart(fig, use_container_width=True)

# Étape 2: Récupérer les données de la table "Gare"
df_gare = pd.read_sql_query("SELECT * from Gare", conn)

# Étape 3: Récupérer les données de la table "ObjetPerdu"
df_objet = pd.read_sql_query("SELECT * from ObjetPerdu", conn)

# Étape 4: Créer une carte folium centrée sur Paris
#m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
map_html = folium.Map(location=[48.8566, 2.3522], zoom_start=12).get_root().render()

# Étape 5: Calculer le nombre total d'objets perdus pour chaque gare

# for i, row in df_gare.iterrows():
#     nom_gare = row['Nom']
#     freq_2019 = row['Freq_2019']
#     freq_2020 = row['Freq_2020']
#     freq_2021 = row['Freq_2021']
#     freq_2022 = row['Freq_2022']
#     longitude = row['Longitude']
#     latitude = row['Latitude']
    
#     objets_par_gare = {}
#     for annee in ['2019', '2020', '2021', '2022']:#
#         objets_par_gare[annee] = {}
#         for objet in df_objet['TypeObjet'].unique():
#             objets_par_gare[annee][objet] = df_objet[(df_objet['GarePerte'] == nom_gare) & (df_objet['AnneePerte'] == annee) & (df_objet['TypeObjet'] == objet)].shape[0]
    
#     # Étape 6: Ajouter un marqueur à la carte pour chaque gare
#     if st.sidebar.checkbox(nom_gare):
#         if st.sidebar.checkbox('Afficher le nombre d\'objets trouvés par année'):
#             for annee in objets_par_gare.keys():
#                 st.sidebar.write('Année : ', annee)
#                 for objet in objets_par_gare[annee].keys():
#                     st.sidebar.write(objet, ':', objets_par_gare[annee][objet])
#         else:
#             freq = freq_2022
#             st.sidebar.write('Fréquence en 2022:', freq)
            
#         marker = folium.Marker(
#             location=[latitude, longitude],
#             popup=nom_gare + ': ' + str(freq),
#             icon=folium.Icon(color='red')
#         )
#         marker.add_to(m)



# Sélectionner la gare et l'année
nom_gare = st.selectbox("Sélectionner une gare", df_gare["Nom"].unique())
annee = st.selectbox("Sélectionner une année", ["2019", "2020", "2021", "2022"])

# Filtrer les données d'objet pour la gare et l'année sélectionnées
df_objet_filtre = df_objet[(df_objet['GarePerte'] == nom_gare) & (df_objet['AnneePerte'] == annee)]

# Vérifier si les données d'objet filtrées sont vides
if df_objet_filtre.empty:
    st.warning("Aucune donnée disponible pour la gare et l'année sélectionnées.")
else:
    # Calculer le nombre d'objets par type
    objets_par_type = df_objet_filtre.groupby("TypeObjet").size().to_dict()

    # Calculer les fréquences pour chaque année
    freq_2019 = None
    freq_2020 = None
    freq_2021 = None
    freq_2022 = None

    if annee == "2019":
        freq_2019 = df_gare[df_gare["Nom" ] == nom_gare]["Freq_2019"].values[0]
    elif annee == "2020":
        freq_2020 = df_gare[df_gare["Nom"] == nom_gare]["Freq_2020"].values[0]
    elif annee == "2021":
        freq_2021 = df_gare[df_gare["Nom"] == nom_gare]["Freq_2021"].values[0]
    elif annee == "2022":
        freq_2022 = df_gare[df_gare["Nom"] == nom_gare]["Freq_2022"].values[0]


    # Afficher les résultats
    st.write("Nombre d'objets par type pour la gare {} en {} :".format(nom_gare, annee))
    st.write(objets_par_type)

    st.write("Fréquence de la gare {} :".format(nom_gare))
    if freq_2019 is not None:
        st.write(" - En 2019 : {} voyages".format(freq_2019))
    if freq_2020 is not None:
        st.write(" - En 2020 : {} voyages".format(freq_2020))
    if freq_2021 is not None:
        st.write(" - En 2021 : {} voyages".format(freq_2021))
    if freq_2022 is not None:
        st.write(" - En 2022 : {} voyages".format(freq_2022))

        
# Étape 7: Afficher la carte en utilisant la méthode "IFrame" de Streamlit
#map_html = folium.Map(location=[48.8566, 2.3522], zoom_start=12).get_root().render()
st.components.v1.html(map_html, width=800, height=600, scrolling=True)

marker = folium.Marker(
    location=[latitude, longitude],
    popup=nom_gare + ': ' + str("freq"),
    icon=folium.Icon(color='red')
    )
marker.add_to(map_html)

