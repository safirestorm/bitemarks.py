import streamlit as st
import requests as req

api_url = "http://api:8000/restaurants"

@st.dialog("Rediger restaurant")
def rediger_modal(r):
    with st.form(key=f"rediger_{r['id']}"):
        navn = st.text_input("Navn", value=r["name"])
        kategori = st.selectbox("Kategori", ["Restaurant", "Cafe", "Bar", "Point of interest"],
            index=["Restaurant", "Cafe", "Bar", "Point of interest"].index(r["category"]))
        cuisine = st.text_input("Cuisine", value=r["cuisine"])
        lokation = st.text_input("Lokation", value=r["location"])
        rating = st.slider("Rating", 0.0, 5.0, value=float(r["rating"] or 0), step=0.5)
        note = st.text_area("Note", value=r["note"] or "")
        gem = st.form_submit_button("Gem ændringer")

    if gem:
        req.put(f"{api_url}/{r['id']}", json={
            "id": r["id"],
            "name": navn,
            "category": kategori,
            "cuisine": cuisine,
            "location": lokation,
            "rating": rating,
            "note": note
        })
        st.rerun()

st.title("Restauranter")
st.write("Her finder du alle dine gemte steder. Søg efter navn, eller rediger og slet steder direkte i listen.")

response = req.get(api_url)
response.raise_for_status()  # Raise an exception for HTTP errors
restaurants = response.json()

search = st.text_input("Søg efter restaurant")

st.divider()

filtered = [r for r in restaurants if search.lower() in r["name"].lower()]

for r in filtered:
    col1, col2, col3 = st.columns([5, 1, 1])

    with col1:
        st.markdown(f"**{r['name']}** &nbsp; ⭐ {r['rating']}")
        st.caption(f"{r['category']} · {r['cuisine']} · {r['location']}")
        if r["note"]:
            st.markdown(f"<blockquote style='font-size: 0.85em;'>{r['note']}</blockquote>", unsafe_allow_html=True)

    with col2:
        if st.button("Rediger", key=f"rediger_{r['id']}"):
            rediger_modal(r)
    
    with col3:
        if st.button("Slet", key=f"slet_{r['id']}"):
            req.delete(f"{api_url}/{r['id']}")
            st.rerun()
    
    st.divider()