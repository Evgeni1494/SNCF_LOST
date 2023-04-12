import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

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


# Connexion à la base de données
conn = sqlite3.connect('SNCF_LOST.db')
cur = conn.cursor()

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





import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlite3

conn = sqlite3.connect('/home/apprenant/Documents/DEV_IA/SNCF_BRIEF/SNCF_LOST/SNCF_LOST.db')
objet_perdu = pd.read_sql_query("SELECT * from ObjetPerdu", conn)
gare = pd.read_sql_query("SELECT * from Gare", conn)

merged_data = pd.merge(objet_perdu, gare, left_on='GarePerte', right_on='Nom')

fig = go.Figure()

for year in merged_data['AnneePerte'].unique():
    for objet in merged_data['TypeObjet'].unique():
        filtered_data = merged_data[(merged_data['AnneePerte']==year) & (merged_data['TypeObjet']==objet)]
        fig.add_trace(
            go.Scattermapbox(
                lat=filtered_data['Latitude'],
                lon=filtered_data['Longitude'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=filtered_data['Freq_'+year]/10,
                    # color=filtered_data['GarePerte'],
                    colorscale='viridis',
                    opacity=0.7,
                    showscale=True
                ),
                text=filtered_data['Nom'] + '<br>' + 'Fréquentation en '+ year + ': ' + filtered_data['Freq_'+year].astype(str),
                hoverinfo='text'
            )
        )

fig.update_layout(
    mapbox=dict(
        accesstoken='your_mapbox_token',
        center=dict(
            lat=48.856614,
            lon=2.3522219
        ),
        zoom=10
    ),
    title='Objets perdus dans les gares de Paris',
)

st.plotly_chart(fig)



