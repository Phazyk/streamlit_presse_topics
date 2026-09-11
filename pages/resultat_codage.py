import pandas as pd
import re
import numpy as np
import datetime
import streamlit as st
st.set_page_config(layout = "wide")

col1, col2 = st.columns(2)
with col1:
    uploaded_file_article = st.file_uploader("CSV des verbatim", type=["csv"])
if uploaded_file_article is None:
    st.warning("En attente du fichier du codage")
    st.stop()

df_verbatim = pd.read_csv(uploaded_file_article,index_col="Unnamed: 0")
df_article = df_verbatim.drop_duplicates("article_id")[["article_id","titre","texte","journal","annee_mois","genre","annee"]]
df_article = df_article.set_index("article_id",drop=False)
tag_options = list(df_verbatim.tag.unique())
tag = st.selectbox("Cadrage",options=tag_options)

date = st.slider("Période", min_value=df_article["annee"].min(),max_value=df_article["annee"].max(),value=(df_article["annee"].min(),df_article["annee"].max()))

df_verbatim = df_verbatim[df_verbatim["annee"]>=date[0] ]
df_verbatim = df_verbatim[df_verbatim["annee"]<=date[1]]

list_article_id = df_verbatim[df_verbatim["tag"]==tag]["article_id"].unique()

article = st.dataframe(df_article.loc[list_article_id].sort_values("annee_mois"),on_select="rerun",selection_mode = "single-cell",hide_index=True)
try : id = df_article.loc[list_article_id].sort_values("annee_mois").iloc[article.selection["cells"][0][0],0]
except : 
    st.info("Cliquez sur le tableau pour afficher un article.")
    st.stop()
sousdf_verbatim = df_verbatim[df_verbatim["article_id"]==id][df_verbatim["tag"]==tag]
 
article_texte = re.sub("\s+"," ",df_article.loc[id,"texte"])
for verba in sousdf_verbatim["verbatim"]:
    verba = re.sub("\s+"," ",verba)
    article_texte = article_texte.replace(verba,f":red-background[{verba}]")
journal = df_article.loc[id,"journal"]
date = df_article.loc[id,"annee_mois"]

st.subheader(df_article.loc[id,"titre"])
st.badge(f"{journal} - {date}")   
st.write(article_texte) 



