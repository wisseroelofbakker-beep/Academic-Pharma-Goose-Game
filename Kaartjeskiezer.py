
import streamlit as st
import random

# Voorbeelddata met vragen en antwoorden
kaartjes = {
    "Fase 1": {
        "Vraag": [
            {"vraag": "Wat is het doel van preklinisch onderzoek?", "antwoord": "Het doel is om de veiligheid en werkzaamheid van een geneesmiddel te testen in diermodellen voordat het op mensen wordt toegepast."},
            {"vraag": "Welke modellen worden gebruikt in dierstudies?", "antwoord": "Vaak worden muizen, ratten of andere kleine dieren gebruikt om toxiciteit en effectiviteit te beoordelen."}
        ],
        "Positief gevolg": [
            "Je muizenstudie toont geen bijwerkingen – ga 2 vakjes vooruit.",
            "Je ontvangt extra subsidie voor je dierstudie – sla een beurt over."
        ],
        "Negatief gevolg": [
            "Er wordt een onverwachte bijwerking gevonden – wacht 1 beurt.",
            "Je moet een extra toxiciteitsstudie uitvoeren – ga 1 vakje terug."
        ]
    },
    "Fase 2": {
        "Vraag": [
            {"vraag": "Wat is een dose-finding studie?", "antwoord": "Een studie om de optimale dosering van een geneesmiddel te bepalen."},
            {"vraag": "Waarom is randomisatie belangrijk in fase 2?", "antwoord": "Om bias te voorkomen en betrouwbare resultaten te verkrijgen."}
        ],
        "Positief gevolg": [
            "Je vindt een optimale dosering – gooi nog een keer.",
            "Je studie toont goede werkzaamheid – ga 2 vakjes vooruit."
        ],
        "Negatief gevolg": [
            "Onvoldoende effect bij lage dosering – ga 1 vakje terug.",
            "Een patiënt stopt vroegtijdig – wacht 1 beurt."
        ]
    }
}

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

