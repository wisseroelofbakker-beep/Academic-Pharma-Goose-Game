import streamlit as st
import pandas as pd
import random

# --------------------------------------------------
# PAGINA-INSTELLINGEN
# --------------------------------------------------

st.set_page_config(
    page_title="Kaartjeskiezer – Academic Pharma",
    page_icon="🎲"
)

# --------------------------------------------------
# EXCEL INLEZEN
# --------------------------------------------------

excel_file = "Academic Pharma Game cards (Antwoorden).xlsx"

df = pd.read_excel(
    excel_file,
    sheet_name=0,
    engine="openpyxl"
)

# --------------------------------------------------
# KOLOMMEN HERNOEMEN
# --------------------------------------------------

df = df.rename(columns={
    "Your card is about which phase?": "Fase",
    "What kind of card are you providing?": "Kaarttype",
    "Provide here a Question or a positive / negative story (side 1 of the card)": "Zijde1",
    "Provide here the answer or the negative or positive consequence (side 2 of the card)": "Zijde2"
})

# --------------------------------------------------
# LEGE WAARDEN OPVULLEN
# --------------------------------------------------

df["Kaarttype"] = df["Kaarttype"].fillna("")
df["Fase"] = df["Fase"].fillna("")
df["Zijde1"] = df["Zijde1"].fillna("")
df["Zijde2"] = df["Zijde2"].fillna("")

# --------------------------------------------------
# KAARTTYPE NORMALISEREN
# --------------------------------------------------

def normaliseer_kaarttype(kaarttype):

    kaarttype = str(kaarttype).lower()

    if "red" in kaarttype:
        return "Negatief gevolg"

    elif "green" in kaarttype:
        return "Positief gevolg"

    elif "black" in kaarttype:
        return "Vraag"

    else:
        return "Onbekend"

df["Kaarttype_norm"] = df["Kaarttype"].apply(
    normaliseer_kaarttype
)

# --------------------------------------------------
# KAARTJES OPBOUWEN
# --------------------------------------------------

kaartjes = {}

for _, row in df.iterrows():

    fase = str(row["Fase"]).strip()

    if fase == "":
        continue

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

        kaartjes[fase]["Vraag"].append({
            "vraag": zijde1,
            "antwoord": zijde2
        })

    elif kaarttype == "Positief gevolg":

        kaartjes[fase]["Positief gevolg"].append(
            f"{zijde1}\n{zijde2}"
        )

    elif kaarttype == "Negatief gevolg":

        kaartjes[fase]["Negatief gevolg"].append(
            f"{zijde1}\n{zijde2}"
        )

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.image(
    "https://raw.githubusercontent.com/wisseroelofbakker-beep/Academic-Pharma-Goose-Game/main/Icon_Academic_Pharma.png",
    width=200
)

st.title("🎲 Kaartjeskiezer – Academic Pharma Bordspel")

# --------------------------------------------------
# CONTROLE OF ER KAARTEN ZIJN
# --------------------------------------------------

if len(kaartjes) == 0:
    st.error("Er zijn geen kaartjes gevonden.")
    st.stop()

# --------------------------------------------------
# SELECTIES
# --------------------------------------------------

fase = st.selectbox(
    "Kies een fase:",
    sorted(list(kaartjes.keys()))
)

kaart_type
