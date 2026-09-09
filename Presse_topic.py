import pandas as pd
import re
import numpy as np
import datetime
import streamlit as st
st.set_page_config(layout = "wide")
col1, col2 = st.columns(2)
with col1:
    uploaded_file_article = st.file_uploader("CSV des articles", type=["csv"])
if uploaded_file_article is None:
    st.warning("En attente du fichier d'articles")
    st.stop()
    
with col2:
    uploaded_file_topics = st.file_uploader("CSV des topics", type=["csv"])
if uploaded_file_topics is None:
    st.warning("En attente du fichier de topics")
    st.stop()

topics = pd.read_csv(uploaded_file_topics,index_col = "Unnamed: 0")
df = pd.read_csv(uploaded_file_article,index_col="Unnamed: 0.1")
n_topic = st.number_input("Topic",min_value=0,max_value=len(topics.columns)-1)


st.dataframe(topics[f"Topic {n_topic}"])
genre = st.segmented_control("Genre",options=["PQR","Nationale","All"],default="All",required=True)
date = st.slider("Période", min_value=df["annee"].min(),max_value=df["annee"].max(),value=(df["annee"].min(),df["annee"].max()))

    
data = df.sort_values(f"topic_{n_topic}",ascending=False)
data = data[data["annee"]>=date[0] ]
data = data[data["annee"]<=date[1]]
if genre != "All":
    data = data[data["genre"]==genre]
article = st.dataframe(data[["journal","titre","date",f"topic_{n_topic}"]],on_select="rerun",selection_mode = "single-cell",hide_index=True)


try : ligne = article.selection["cells"][0][0]
except : 
    st.info("Cliquez sur le tableau pour afficher un article.")
    st.stop()
def replace_ele(x):
    return ":orange-background[{}]".format(x.group())
texte = data.iloc[int(ligne),4]
if st.toggle("Électrique",value = True):
    texte=re.sub("électriques?",replace_ele,texte,count=0,flags=re.IGNORECASE)
st.subheader(f"{data.iloc[ligne,1]}")
st.badge(f"{data.iloc[ligne,2]} - {data.iloc[ligne,7]}")

st.write(texte)



