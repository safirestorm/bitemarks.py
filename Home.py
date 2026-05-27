import streamlit as st
import requests as req
import pydeck as pdk
import pandas as pd

api_url = "http://api:8000/restaurants"

st.title("Bitemarks")
st.write("Velkommen til Bitemarks — " \
"stedet hvor du samler dine madoplevelser. Tilføj restauranter, caféer og barer du har besøgt, " \
"giv dem en rating og find dem på kortet. Har du et sted du gerne vil prøve? " \
"Gem det som et Point of Interest og vend tilbage til det senere.")

if "form_key" not in st.session_state:
    st.session_state.form_key = 0

with st.form(f"tilføj_restaurant_{st.session_state.form_key}"):
    st.subheader("Tilføj Restaurant")
    name = st.text_input("Navn")
    category = st.selectbox("Kategori", ["Restaurant", "Café", "Bar", "Fastfood", "Point of interest"])
    cuisine = st.text_input("Cuisine")
    location = st.text_input("Lokation")
    rating = st.slider("Rating", 0.0, 5.0, step=0.5)
    note = st.text_area("Note")
    save = st.form_submit_button("Tilføj restaurant")

if save:
    if not name or not location or not cuisine:
        if not name:
            st.error("Du mangler at tilføje et navn.")
        if not location:
            st.error("Du mangler at tilføje en adresse.")
        if not cuisine:
            st.error("Du mangler at tilføje cuisine.")
    else:
        req.post(api_url, json={
            "id": 0,
            "name": name,
            "category": category,
            "cuisine": cuisine,
            "location": location,
            "rating": rating,
            "note": note
        })
        st.success("Restaurant tilføjet!")
        st.session_state.form_key += 1
        st.rerun()

st.divider()
st.subheader("Kort")

response = req.get(api_url)
response.raise_for_status()  # Raise an exception for HTTP errors
restaurants = response.json()
df = pd.DataFrame(restaurants)
# Tilføj kolonner hvis de mangler
if "lat" not in df.columns:
    df["lat"] = None
if "lng" not in df.columns:
    df["lng"] = None

# Kun vis restauranter der har koordinater
df_map = df[df["lat"].notna() & df["lng"].notna()]

if len(df_map) == 0:
    st.info("Ingen restauranter med koordinater endnu.")
else:
    st.pydeck_chart(pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
        initial_view_state=pdk.ViewState(
            latitude=df_map["lat"].mean(),
            longitude=df_map["lng"].mean(),
            zoom=12
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df_map,
                get_position="[lng, lat]",
                get_radius=8,
                radius_units="pixels",
                get_fill_color=[255, 75, 75],
                pickable=True
            )
        ],
        tooltip={"text": "{name}\n{category} — {cuisine}\n⭐ {rating}"}
    ))