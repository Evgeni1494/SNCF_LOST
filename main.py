import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
from utils import Objet_type_semaine,Objet_semaine,Paris_map,Temp_Objet,Saison_Objet_med,Saison_type_objet


# Se connecter à la base de données
conn = sqlite3.connect('SNCF_LOST.db')
cur = conn.cursor()

############################################### Graphique Objets trouvés par semaine par type d'objets ####################

Objet_type_semaine()

########################################## Graphique Objets trouvé par semaine ##########################################

Objet_semaine()
############################################## GARES DE PARIS AVEC GARE ET NOMBRE D'OBJETS TROUVE ##################

Paris_map()

########################################### GRAPH Temperature sur Objet ###############################
Temp_Objet()

############################################ Graph Saison mediane Objet ###############################################
Saison_Objet_med()

############################################ Graph Saison type d'objet ##################################################
Saison_type_objet()


conn.close()