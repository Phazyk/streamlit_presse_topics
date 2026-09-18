import pandas as pd
import re
import numpy as np
import datetime
from datetime import datetime
import streamlit as st


if "article_topic" not in st.session_state:
    st.session_state.article_topic = pd.DataFrame()

if len(st.session_state.article_topic)==0:
    st.warning("En attente du fichier d'articles sur la page \"Presse topic\"")
    st.stop()



df = st.session_state.article_topic
df["acteur"]=df["acteur"].fillna("")
df["annee_mois"] = pd.to_datetime(df["annee_mois"],format="mixed",utc=True)

option_genre = list(df.genre.unique())
option_genre.append("Tout")

recherche = "N/A"
col1, col2 = st.columns([1,1])
with col1:
#Sélection des variables
    genre = st.segmented_control("Genre",option_genre,default="Tout")
    periode = st.slider("Période", min_value=df["annee"].min(),max_value=df["annee"].max(),value=(df["annee"].min(),df["annee"].max()))

with col2:
    ou_et = st.selectbox("Opérateur logique entre les mots-clés",["OU","ET"])

    keyword = st.text_input("Mots-clés",label_visibility="visible",help="Liste de mots-clés séparés par une virgule")

keyword = re.sub("\s*,\s",",",keyword)
df["recherche"] = 0
for mot in keyword.split(","):
    df["recherche"] += df["texte"].apply(lambda x: not re.search(mot,x,re.IGNORECASE)==None)


df_afficher = df[(df["annee"]>=periode[0]) & (df["annee"]<=periode[1])]

if genre!="Tout":
    df_afficher = df[df["genre"]==genre]

if ou_et == "OU":
    df_afficher = df_afficher[df["recherche"]!=0]
else : df_afficher = df_afficher[df["recherche"]==len(keyword.split(","))]



df_afficher = df_afficher[["titre","nb_occurences","annee_mois","journal","texte"]].sort_values("annee_mois")

st.write("nombre d'articles : "+str(len(df_afficher)))

selection_article = st.dataframe(df_afficher,on_select="rerun",selection_mode = "single-cell",hide_index=True)
try : ligne = selection_article.selection["cells"][0][0]
except : 
    st.info("Cliquez sur le tableau pour afficher un article.")
    st.stop()

col3, col4, col5 = st.columns([0.15,0.15,0.7])
def replace_ele(x):
    return ":orange-background[{}]".format(x.group())
def replace_search(x):
    return ":red-background[{}]".format(x.group())
with col3:
    ele=st.toggle("Électrique",value=True)
with col4:
    search=st.toggle("Mots-clés",value=True)
try:
    
    texte = df_afficher.iloc[int(ligne),4]
    if ele:
        texte=re.sub("électriques?",replace_ele,texte,count=0,flags=re.IGNORECASE)
    if search:
        if keyword!="":
            for mot in keyword.split(","):
                texte=re.sub(mot,replace_search,texte,count=0,flags=re.IGNORECASE)
    #with col3:
        #st.code(article,language="python")
    st.subheader(df_afficher.iloc[int(ligne),0])
    date = df_afficher.iloc[ligne,2].strftime("%d %B %Y")
    st.badge(f"{df_afficher.iloc[ligne,3]} - {date}")
    st.markdown(texte)
except IndexError: print("eh")
