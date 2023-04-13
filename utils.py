import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import folium_static

############################################### Graphique Objets trouvés par semaine par type d'objets ####################
# Se connecter à la base de données
conn = sqlite3.connect('SNCF_LOST.db')
cur = conn.cursor()

def Objet_type_semaine():
    """
    Cette fonction récupère la liste des types d'objets disponibles dans la table "ObjetPerdu" 
    et affiche une liste déroulante permettant de sélectionner les types d'objets à inclure dans l'histogramme. 
    Elle calcule ensuite la somme des objets trouvés par semaine entre 2019 et 2022 pour chaque type d'objet sélectionné, 
    filtre les données en fonction des types d'objets sélectionnés et affiche l'histogramme avec Plotly.

    Returns:
    La fonction affiche l'histogramme des objets trouvés par semaine entre 2019 et 2022 pour chaque type d'objet sélectionné.
    """
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
    fig = px.histogram(df_objets, x='Semaine', y='NbObjets',width=1000,height=500, color='TypeObjet', nbins=len(df_objets['Semaine'].unique()), labels={'Semaine': 'Semaine (année-mois-jour)', 'NbObjets': 'Nombre d\'objets trouvés'})

    fig.update_layout(
        xaxis_title="Semaine",
        yaxis_title="Nombre d'objets trouvés",
        title="Répartition du nombre d'objets trouvés par semaine entre 2019 et 2022 par type d'objet.")
    return st.plotly_chart(fig)



########################################## Graphique Objets trouvé par semaine ##########################################

def Objet_semaine():
    """
    Cette fonction récupère le nombre d'objets trouvés par semaine entre 2019 et 2022 dans la table "ObjetPerdu". 
    Elle crée ensuite un histogramme avec Plotly pour représenter la répartition du nombre d'objets trouvés par semaine. 
    Enfin, elle affiche l'histogramme à l'aide de Streamlit.

    Returns:
    La fonction affiche l'histogramme du nombre d'objets trouvés par semaine entre 2019 et 2022.
    """
    conn = sqlite3.connect('SNCF_LOST.db')
    # Requête SQL pour récupérer le nombre d'objets trouvés par semaine
    query = """
    SELECT strftime('%Y-%M-%W', Date) AS Semaine, COUNT(*) AS NbObjets
    FROM ObjetPerdu
    WHERE AnneePerte >= 2019 AND AnneePerte <= 2022
    GROUP BY Semaine
    """

    # Récupération des données dans un DataFrame pandas
    df = pd.read_sql_query(query, conn)

    # Création du graphique avec Plotly
    fig = px.histogram(df, x="Semaine", y="NbObjets", nbins=len(df), width=1000, height=500)
    fig.update_layout(
        xaxis_title="Semaine",
        yaxis_title="Nombre d'objets trouvés",
        title="Répartition du nombre d'objets trouvés par semaine entre 2019 et 2022."
    )

    # Affichage du graphique avec Streamlit
    return st.plotly_chart(fig, use_container_width=True)

############################################## GARES DE PARIS AVEC FREQUENTATION ET NOMBRE D'OBJETS TROUVE ##################
def Paris_map():
    """
    Affiche une carte de Paris avec des marqueurs pour chaque gare où des objets perdus ont été trouvés,
    en fonction de l'année et du type d'objet choisi par l'utilisateur.

    Returns:
        folium.folium.Map:
            La carte générée par Folium avec des marqueurs indiquant les gares où des objets perdus ont été trouvés,
            en fonction de l'année et du type d'objet sélectionné.

    """
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
    df_filtered_grouped = df_filtered.groupby(['GarePerte']).count().reset_index()
    df_filtered_grouped = df_filtered_grouped[['GarePerte', 'TypeObjet']]
    df_filtered_grouped = df_filtered_grouped.rename(columns={'TypeObjet': 'NbObjets'})
    df_filtered = df_filtered.merge(df_filtered_grouped, on='GarePerte', how='left')

    
    # Création des marqueurs sur la carte
    for index, row in df_filtered.iterrows():
        popup_text = "Gare : " + row['Nom'] + "<br>" + "Fréquentation " + year + " : " + str(row['Freq_'+year]) + "<br>" + "Nombre de " + obj_type + " : " + str(row['NbObjets'])
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup_text).add_to(m)

    # Affichage de la carte sur Streamlit
    st.title("Carte des objets perdus dans les gares de Paris")
    st.sidebar.title("Paramètres de la carte de Paris")
    st.sidebar.write("Année choisie :", year)
    st.sidebar.write("Type d'objet choisi :", obj_type)
    return folium_static(m)




def Temp_Objet():
    """
    Cette fonction récupère depuis une base de données SQL le nombre d'objets trouvés et la température moyenne, 
    en joignant les tables "ObjetPerdu" et "Temperature" sur la colonne "Date".
    
    Elle crée ensuite un scatterplot avec Seaborn pour représenter graphiquement la corrélation entre 
    le nombre d'objets trouvés et la température moyenne.

    Returns:
    - Le scatterplot créé avec Seaborn.
    - Une intérpretation.
    """
    # Requête SQL pour récupérer le nombre d'objets trouvés et la température moyenne
    # en joignant les tables "ObjetPerdu" et "Temperature" sur la colonne "Date"
    conn = sqlite3.connect('SNCF_LOST.db')
    cur = conn.cursor() 

    query = """
    SELECT Temperature.TempMed, COUNT(ObjetPerdu.id) AS count_objet
    FROM ObjetPerdu
    JOIN Temperature ON ObjetPerdu.Date = Temperature.Date
    GROUP BY Temperature.TempMed
    """

    # Exécution de la requête SQL
    cur.execute(query)

    # Récupération des résultats de la requête
    results = cur.fetchall()

    # Création du scatterplot avec Seaborn
    sns.set(style='darkgrid')
    fig, ax = plt.subplots()
    sns.scatterplot(x=[result[0] for result in results], y=[result[1] for result in results], ax=ax)
    plt.xlabel('Température moyenne')
    plt.ylabel('Nombre d\'objets trouvés')
    plt.title("Nombre d'objets trouvé selon la temperature moyenne")
    


    return st.pyplot(fig), st.write(" D'après le graphique le nombre d'objets perdus semble corrélé a la temperature. On peut voir que la distribution suit la loi normale.")

def Saison_Objet_med():
    """
    Calcule la médiane du nombre d'objets trouvés par saison et affiche un boxplot avec les résultats.
    
    Returns:
    -------
    fig : objet matplotlib.pyplot
        Boxplot représentant la distribution des nombres d'objets trouvés par saison.
    message : str
        Interpretation.
    """
    conn = sqlite3.connect('SNCF_LOST.db')
    cur = conn.cursor()
    # Requête SQL pour calculer la médiane du nombre d'objets trouvés par saison
    query = """
    SELECT CASE WHEN strftime('%m', ObjetPerdu.Date) IN ('12','01','02') THEN 'Hiver'
                WHEN strftime('%m', ObjetPerdu.Date) IN ('03','04','05') THEN 'Printemps'
                WHEN strftime('%m', ObjetPerdu.Date) IN ('06','07','08') THEN 'Été'
                WHEN strftime('%m', ObjetPerdu.Date) IN ('09','10','11') THEN 'Automne' END AS season,
        COUNT(id) AS count_objet
    FROM ObjetPerdu
    GROUP BY season
    """

    # Exécution de la requête SQL
    cur.execute(query)

    # Récupération des résultats de la requête
    results = cur.fetchall()

    # Création du boxplot avec Matplotlib
    labels = ['Hiver', 'Printemps', 'Été', 'Automne']
    data = [[result[1] for result in results if result[0] == label] for label in labels]
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    plt.xlabel('Saison')
    plt.ylabel('Nombre d\'objets trouvés')
    plt.title("Nombre median d'objets trouvé par saison")
    

    return st.pyplot(fig),st.write("Il semble avoir une corrélation entre la mèdiane des objets trouvés et la saison car les mèdianes sont trés differentes les unes des autres. ")



def Saison_type_objet():
    """
    Compte le nombre d'objets trouvés par saison et par type d'objet, affiche un graphique barres avec les résultats.

    Returns:
    -------
    fig : objet matplotlib.pyplot
        Graphique représentant la distribution des nombres d'objets trouvés par saison pour un type d'objet donné.
    message : str
        Interpretation.
    """
    # Requête SQL pour compter le nombre d'objets trouvés par saison et par type d'objet
    conn = sqlite3.connect('SNCF_LOST.db')
    cur = conn.cursor()
    query = """
    SELECT CASE WHEN strftime('%m', ObjetPerdu.Date) IN ('12','01','02') THEN 'Hiver'
                WHEN strftime('%m', ObjetPerdu.Date) IN ('03','04','05') THEN 'Printemps'
                WHEN strftime('%m', ObjetPerdu.Date) IN ('06','07','08') THEN 'Été'
                WHEN strftime('%m', ObjetPerdu.Date) IN ('09','10','11') THEN 'Automne' END AS season,
        TypeObjet,
        COUNT(id) AS count_objet
    FROM ObjetPerdu
    GROUP BY season, TypeObjet
    """

    # Exécution de la requête SQL
    cur.execute(query)

    # Récupération des résultats de la requête
    results = cur.fetchall()

    # Préparation des données pour l'affichage
    labels = ['Hiver', 'Printemps', 'Été', 'Automne']
    types_objet = list(set(result[1] for result in results))
    data = {type_objet: [result[2] for result in results if result[1] == type_objet] for type_objet in types_objet}

    # Interface utilisateur Streamlit pour sélectionner le type d'objet
    selected_type_objet = st.selectbox('Sélectionnez un type d\'objet', types_objet)

    # Filtrer les données en fonction du type d'objet sélectionné
    filtered_data = {season: data[selected_type_objet][i] if i < len(data[selected_type_objet]) else 0 for i, season in enumerate(labels)}

    # Création du graphique
    fig, ax = plt.subplots()
    ax.bar(filtered_data.keys(), filtered_data.values())

    ax.set_xlabel('Saison')
    ax.set_ylabel('Nombre d\'objets trouvés')
    ax.set_title(f'Nombre d\'objets trouvés en fonction de la saison pour les objets de type "{selected_type_objet}"')
    fig.set_size_inches(10, 6)
    # Affichage du graphique dans Streamlit
    

    return st.pyplot(fig), st.write("Il semble y avoir une corrélation entre le type d'objet perdu et la saison. En effet selon les saisons les objets que les gens transportent et donc risquent de perdre changeant. Un des exemples parlant serait le 'Snowboard'")

