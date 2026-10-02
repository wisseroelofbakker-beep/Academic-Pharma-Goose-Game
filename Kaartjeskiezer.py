
import streamlit as st
import pandas as pd
import random

# Laad de kaartjes uit het Excel-bestand
excel_file = "Academic Pharma Game cards (Antwoorden).xlsx"
df = pd.read_excel(excel_file, sheet_name=0, engine="openpyxl")

# Hernoem kolommen voor duidelijkheid
df = df.rename(columns={
    "Your card is about which phase?": "Fase",
    "What kind of card are you providing?": "Kaarttype",
    "Provide here a Question or a positive / negative story (side 1 of the card)": "Zijde1",
    "Provide here the answer or the negative or positive consequence (side 2 of the card)": "Zijde2"
})

# Lege waarden opvullen
df["Kaarttype"] = df["Kaarttype"].fillna("")

# Functie om kaarttype te normaliseren
def normaliseer_kaarttype(kaarttype):

    kaarttype = str(kaarttype)

    if "Negative" in kaarttype:
        return "Negatief gevolg"

    elif "Positive" in kaarttype:
        return "Positief gevolg"

    elif "Question" in kaarttype:
        return "Vraag"

    else:
        return "Onbekend"

# Nieuwe kolom maken
df["Kaarttype_norm"] = df["Kaarttype"].apply(
    normaliseer_kaarttype
)

st.write(df["Kaarttype"].unique())
st.write(df["Kaarttype_norm"].value_counts())

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
        st.markdown(
            f"""
            <div style="background-color:#333333;color:white;padding:15px;border-radius:10px">
            <strong>Vraag – {fase}</strong><br><br>
            {st.session_state.gekozen_kaart['vraag']}
            </div>
            """,
            unsafe_allow_html=True
        )
    elif kaart_type == "Positief gevolg":
        gekozen_kaart = random.choice(kaartjes[fase][kaart_type])
        st.markdown(
            f"""
            <div style="background-color:#ccffcc;padding:15px;border-radius:10px">
            <strong>Positief gevolg – {fase}</strong><br><br>
            {gekozen_kaart.replace('\n', '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )
    elif kaart_type == "Negatief gevolg":
        gekozen_kaart = random.choice(kaartjes[fase][kaart_type])
        st.markdown(
            f"""
            <div style="background-color:#ffcccc;padding:15px;border-radius:10px">
            <strong>Negatief gevolg – {fase}</strong><br><br>
            {gekozen_kaart.replace('\n', '<br>')}
            </div>
            """,
            unsafe_allow_html=True
        )

if kaart_type == "Vraag" and st.session_state.gekozen_kaart:
    if st.button("Toon antwoord"):
        st.success(f"Antwoord: {st.session_state.gekozen_kaart['antwoord']}")

