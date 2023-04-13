import sqlite3
import matplotlib.pyplot as plt
import streamlit as st

# Connexion à la base de données
conn = sqlite3.connect('SNCF_LOST.db')
c = conn.cursor()

# Requête SQL pour compter le nombre d'objets trouvés par saison et par type d'objet
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
c.execute(query)

# Récupération des résultats de la requête
results = c.fetchall()

# Fermeture de la connexion à la base de données
conn.close()

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
st.pyplot(fig)




