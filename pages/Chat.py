import os
import streamlit as st
import requests as req
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
api_url = "http://api:8000/restaurants"

st.title("Anbefalinger")
st.write("Få personlige madanbefalinger baseret på de steder du har besøgt og givet en rating.")

restaurants = req.get(api_url).json()
restaurant_liste = "\n".join([
    f"- {r['name']} ({r['category']}, {r['cuisine']}) — rating: {r['rating']}"
    for r in restaurants
])

system_prompt = f"""Du er en madanbefalings-assistent.
Du hjælper kun med spørgsmål om mad, restauranter og anbefalinger.
Hvis brugeren spørger om noget andet, afvis venligt og bring samtalen tilbage til mad.

Brugerens besøgte restauranter:
{restaurant_liste}

Brug denne historik til at give personlige anbefalinger."""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Spørg om madanbefalinger..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = req.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
        json={
            "model": "mistral-large-latest",
            "messages": [{"role": "system", "content": system_prompt}] + st.session_state.messages
        }
    )

    svar = response.json()["choices"][0]["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": svar})
    with st.chat_message("assistant"):
        st.write(svar)
