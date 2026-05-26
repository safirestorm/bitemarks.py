import streamlit as st
import requests as req
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("Solarize_Light2")

api_url = "http://api:8000/restaurants"

st.title("Statistik")
st.write("Et overblik over dine besøg og ratings.")

restaurants = req.get(api_url).json()

if len(restaurants) == 0:
    st.info("Ingen restauranter endnu — tilføj nogle på forsiden!")
else:
    df_alle = pd.DataFrame(restaurants)
    df = df_alle[df_alle["category"] != "Point of interest"]

    ratings = df["rating"].dropna().values
    st.subheader("Overblik")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gennemsnitlig rating", round(np.mean(ratings), 2))
    col2.metric("Antal steder", len(df_alle))
    col3.metric("Favorit cuisine", df["cuisine"].value_counts().index[0])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Antal restauranter per kategori")
        antal_per_kategori = df.groupby("category").size()
        fig, ax = plt.subplots()
        ax.bar(antal_per_kategori.index, antal_per_kategori.values, color="#E67E22")
        ax.set_xlabel("Kategori")
        ax.set_ylabel("Antal")
        st.pyplot(fig)

    with col2:
        st.subheader("Gennemsnitlig rating per kategori")
        rating_per_kategori = df.groupby("category")["rating"].mean()
        fig, ax = plt.subplots()
        ax.bar(rating_per_kategori.index, rating_per_kategori.values, color="#E67E22")
        ax.set_xlabel("Kategori")
        ax.set_ylabel("Gennemsnitlig rating")
        ax.set_ylim(0, 5)
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Fordeling af ratings")
        rating_fordeling = df["rating"].value_counts().sort_index()
        fig, ax = plt.subplots()
        ax.bar(rating_fordeling.index, rating_fordeling.values, color="#E67E22")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Antal")
        st.pyplot(fig)

    with col4:
        st.subheader("Fordeling af cuisine")
        cuisine_fordeling = df_alle["cuisine"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(cuisine_fordeling.values, labels=cuisine_fordeling.index, autopct="%1.1f%%")
        st.pyplot(fig)