"""
pages/apropos.py  ->  Page "A propos"
-------------------------------------
Presentation du projet, de l'auteur et de la stack technique.
"""

from __future__ import annotations

import streamlit as st

from utils.theme import page_header, section_title


def render() -> None:
    page_header("A propos", "Projet academique - Sciences de Donnees Medicales")

    section_title("Le projet")
    st.markdown(
        "Cette application web interactive est dediee a l'**analyse**, au "
        "**nettoyage** et au **pretraitement** de donnees medicales. "
        "Le sujet retenu est l'**analyse des donnees COVID-19** "
        "(donnees cliniques de patients)."
    )

    section_title("Auteur")
    st.markdown(
        "- **Nom :** Saad Elidrissi El Hassan\n"
        "- **Formation :** 2eme annee Licence - Informatique Decisionnelle "
        "en Sante Digitale\n"
        "- **Etablissement :** UM6SS - Ecole Superieure Mohammed VI "
        "d'Ingenieurs en Sciences de la Sante"
    )

    section_title("Stack technique")
    st.markdown(
        "- **Python** : langage principal\n"
        "- **Streamlit** : interface web interactive\n"
        "- **Pandas / NumPy** : manipulation et calcul numerique\n"
        "- **Plotly** : graphiques interactifs\n"
        "- **Matplotlib** : graphiques exportables (PNG)\n"
        "- **OpenPyXL** : export Excel"
    )

    section_title("Fonctionnalites")
    st.markdown(
        "Importation CSV, analyse exploratoire (statistiques, correlations, "
        "distributions, valeurs manquantes, doublons), preprocessing complet "
        "(imputation, outliers, encodage, normalisation, filtrage), "
        "visualisations interactives, exportation (CSV, Excel, PNG, rapport), "
        "mode sombre, historique des traitements, comparaison avant/apres, "
        "et tableau de bord analytique."
    )

    st.caption("Saad Elidrissi El Hassan. Projet academique.")
