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

excel_file = "Academic Pharma Game cards (Antwoorden) extended.xlsx"

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
# SESSION STATE
# --------------------------------------------------

if "gekozen_kaart" not in st.session_state:
    st.session_state.gekozen_kaart = None

if "decks" not in st.session_state:
    st.session_state.decks = {}

# --------------------------------------------------
# FUNCTIE: TREK KAART ZONDER DUPLICATEN
# --------------------------------------------------

def trek_kaart_zonder_duplicaten(fase, kaart_type):

    sleutel = f"{fase}_{kaart_type}"

    kaarten = kaartjes[fase][kaart_type]

    if (
        sleutel not in st.session_state.decks
        or len(st.session_state.decks[sleutel]) == 0
    ):

        st.session_state.decks[sleutel] = kaarten.copy()

        random.shuffle(
            st.session_state.decks[sleutel]
        )

    return st.session_state.decks[sleutel].pop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.image(
    "https://raw.githubusercontent.com/wisseroelofbakker-beep/Academic-Pharma-Goose-Game/main/Icon_Academic_Pharma.png",
    width=200
)

st.title("🎲 Kaartjeskiezer – Academic Pharma Bordspel")

# --------------------------------------------------
# SELECTIES
# --------------------------------------------------

fase = st.selectbox(
    "Kies een fase:",
    sorted(list(kaartjes.keys()))
)

kaart_type = st.selectbox(
    "Kies een type kaartje:",
    [
        "Vraag",
        "Positief gevolg",
        "Negatief gevolg"
    ]
)

# --------------------------------------------------
# KAARTTELLER
# --------------------------------------------------

sleutel = f"{fase}_{kaart_type}"

totaal = len(
    kaartjes[fase][kaart_type]
)

if sleutel in st.session_state.decks:
    resterend = len(
        st.session_state.decks[sleutel]
    )
else:
    resterend = totaal

st.info(
    f"📚 Nog {resterend} van de {totaal} kaarten beschikbaar in deze stapel."
)

# --------------------------------------------------
# RESET KNOP
# --------------------------------------------------

if st.button("🔄 Reset alle kaartstapels"):

    st.session_state.decks = {}
    st.session_state.gekozen_kaart = None

    st.success(
        "Alle kaartstapels zijn opnieuw geschud."
    )

# --------------------------------------------------
# TREK KAART
# --------------------------------------------------

if st.button("🎲 Trek een kaartje"):

    st.session_state.gekozen_kaart = None

    beschikbare_kaarten = kaartjes[fase][kaart_type]

    if len(beschikbare_kaarten) == 0:

        st.error(
            f"Er zijn geen '{kaart_type}' kaarten beschikbaar voor '{fase}'."
        )

    else:

        # ------------------------------
        # VRAAG
        # ------------------------------

        if kaart_type == "Vraag":

            st.session_state.gekozen_kaart = (
                trek_kaart_zonder_duplicaten(
                    fase,
                    kaart_type
                )
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#333333;
                    color:white;
                    padding:15px;
                    border-radius:10px;">
                    <strong>Vraag – {fase}</strong><br><br>
                    {st.session_state.gekozen_kaart['vraag']}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ------------------------------
        # POSITIEF
        # ------------------------------

        elif kaart_type == "Positief gevolg":

            gekozen_kaart = (
                trek_kaart_zonder_duplicaten(
                    fase,
                    kaart_type
                )
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#ccffcc;
                    padding:15px;
                    border-radius:10px;">
                    <strong>Positief gevolg – {fase}</strong><br><br>
                    {gekozen_kaart.replace(chr(10), '<br>')}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ------------------------------
        # NEGATIEF
        # ------------------------------

        elif kaart_type == "Negatief gevolg":

            gekozen_kaart = (
                trek_kaart_zonder_duplicaten(
                    fase,
                    kaart_type
                )
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#ffcccc;
                    padding:15px;
                    border-radius:10px;">
                    <strong>Negatief gevolg – {fase}</strong><br><br>
                    {gekozen_kaart.replace(chr(10), '<br>')}
                </div>
                """,
                unsafe_allow_html=True
            )

# --------------------------------------------------
# ANTWOORD TONEN
# --------------------------------------------------

if (
    kaart_type == "Vraag"
    and st.session_state.gekozen_kaart is not None
):

    if st.button("✅ Toon antwoord"):

        st.success(
            st.session_state.gekozen_kaart["antwoord"]
        )


# --------------------------------------------------
# KAART TREKKEN
# --------------------------------------------------

if st.button("🎲 Trek een kaartje"):

    beschikbare_kaarten = kaartjes[fase][kaart_type]

    if len(beschikbare_kaarten) == 0:
        st.error(
            f"Er zijn geen '{kaart_type}' kaarten beschikbaar voor '{fase}'."
        )
    else:

        if kaart_type == "Vraag":

            st.session_state.gekozen_kaart = random.choice(
                beschikbare_kaarten
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#333333;
                    color:white;
                    padding:15px;
                    border-radius:10px;">
                    <strong>Vraag – {fase}</strong><br><br>
                    {st.session_state.gekozen_kaart['vraag']}
                </div>
                """,
                unsafe_allow_html=True
            )

        elif kaart_type == "Positief gevolg":

            gekozen_kaart = random.choice(
                beschikbare_kaarten
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#ccffcc;
                    padding:15px;
                    border-radius:10px;">
                    <strong>Positief gevolg – {fase}</strong><br><br>
                    {gekozen_kaart.replace(chr(10), '<br>')}
                </div>
                """,
                unsafe_allow_html=True
            )

        elif kaart_type == "Negatief gevolg":

            gekozen_kaart = random.choice(
                beschikbare_kaarten
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#ffcccc;
                    padding:15px;
                    border-radius:10px;">
                    <strong>Negatief gevolg – {fase}</strong><br><br>
                    {gekozen_kaart.replace(chr(10), '<br>')}
                </div>
                """,
                unsafe_allow_html=True
            )

# --------------------------------------------------
# ANTWOORD TONEN
# --------------------------------------------------

if (
    kaart_type == "Vraag"
    and st.session_state.gekozen_kaart is not None
):
    if st.button("✅ Toon antwoord"):
        st.success(
            st.session_state.gekozen_kaart["antwoord"]
        )
