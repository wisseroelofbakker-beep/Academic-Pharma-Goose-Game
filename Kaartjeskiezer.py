
import streamlit as st
import random

# Voorbeelddata
kaartjes = {
    "Fase 1": {
        "Vraag": [
            "Wat is het doel van preklinisch onderzoek?",
            "Welke modellen worden gebruikt in dierstudies?"
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
            "Wat is een dose-finding studie?",
            "Waarom is randomisatie belangrijk in fase 2?"
        ],
        "Positief gevolg": [
            "Je vindt een optimale dosering – gooi nog een keer.",
            "Je studie toont goede werkzaamheid – ga 2 vakjes vooruit."
        ],
        "Negatief gevolg": [
            "Onvoldoende effect bij lage dosering – ga 1 vakje terug.",
            "Een patiënt stopt vroegtijdig – wacht 1 beurt."
        ]
    },
    # Voeg Fase 3 t/m 6 toe op dezelfde manier
}

st.title("🎲 Kaartjeskiezer – Academic Pharma Bordspel")

# Selectie van fase en type
fase = st.selectbox("Kies een fase:", list(kaartjes.keys()))
kaart_type = st.selectbox("Kies een type kaartje:", ["Vraag", "Positief gevolg", "Negatief gevolg"])

# Trek een kaartje
if st.button("Trek een kaartje"):
    gekozen_kaart = random.choice(kaartjes[fase][kaart_type])
    st.success(f"**{kaart_type} – {fase}**\n\n{gekozen_kaart}")
