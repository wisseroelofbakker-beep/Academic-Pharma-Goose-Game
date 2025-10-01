
import streamlit as st
import pandas as pd
import random

# Laad de kaartjes uit het Excel-bestand
excel_file = "Academic Pharma Game cards (Antwoorden).xlsx"
df = pd.read_excel(excel_file, sheet_name=0, engine="openpyxl")

# Hernoem kolommen voor duidelijkheid
df.columns = [
    "Tijdstempel",
    "Fase",
    "Zijde1",
    "Zijde2",
    "Kaarttype",
    "Kolom5",
    "Kolom4"
]

# Functie om kaarttype te normaliseren
def normaliseer_kaarttype(kaarttype):
    if "Red" in kaarttype:
        return "Negatief gevolg"
    elif "Green" in kaarttype:
        return "Positief gevolg"
    elif "Black" in kaarttype:
        return "Vraag"
    else:
        return "Onbekend"

# Normaliseer kaarttypes
df["Kaarttype_norm"] = df["Kaarttype"].apply(normaliseer_kaarttype)

# Genereer de kaartjes dictionary
kaartjes = {}
for _, row in df.iterrows():
    fase = row["Fase"]
    kaarttype = row["Kaarttype_norm"]
    zijde1 = str(row["Zijde1"]).strip()
    zijde2 = str(row["Zijde2"]).strip()

    if fase not in kaartjes:
        kaartjes[fase] = {
            "Vraag": [],
            "Positief gevolg": [],
            "Negatief gevolg": []
        }

    if kaarttype == "Vraag":
        kaartjes[fase]["Vraag"].append({"vraag": zijde1, "antwoord": zijde2})
    elif kaarttype in ["Positief gevolg", "Negatief gevolg"]:
        kaartjes[fase][kaarttype].append(f"{zijde1}\n{zijde2}")

# Streamlit-app
st.set_page_config(page_title="Kaartjeskiezer – Academic Pharma", page_icon="🎲")
st.image("https://raw.githubusercontent.com/wisseroelofbakker-beep/Academic-Pharma-Goose-Game/main/Icon_Academic_Pharma.png", width=200)
st.title("🎲 Kaartjeskiezer – Academic Pharma Bordspel")

fase = st.selectbox("Kies een fase:", list(kaartjes.keys()))
kaart_type = st.selectbox("Kies een type kaartje:", ["Vraag", "Positief gevolg", "Negatief gevolg"])

if "gekozen_kaart" not in st.session_state:
    st.session_state.gekozen_kaart = None

if st.button("Trek een kaartje"):
    if kaart_type == "Vraag":
        st.session_state.gekozen_kaart = random.choice(kaartjes[fase][kaart_type])
        st.info(f"**Vraag – {fase}**\n\n{st.session_state.gekozen_kaart['vraag']}")
    else:
        gekozen_kaart = random.choice(kaartjes[fase][kaart_type])
        st.success(f"**{kaart_type} – {fase}**\n\n{gekozen_kaart}")

if kaart_type == "Vraag" and st.session_state.gekozen_kaart:
    if st.button("Toon antwoord"):
        st.success(f"Antwoord: {st.session_state.gekozen_kaart['antwoord']}")

