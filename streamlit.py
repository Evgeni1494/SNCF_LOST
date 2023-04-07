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


