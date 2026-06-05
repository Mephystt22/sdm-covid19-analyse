"""
pages/importation.py  ->  Page "Importation des donnees"
--------------------------------------------------------
Importation d'un fichier CSV (ou chargement du dataset COVID-19 d'exemple),
puis inspection complete : apercu, dimensions, types, statistiques, info
generale, detection num/cat, doublons et memoire.
"""

from __future__ import annotations

import os
import time

import pandas as pd
import streamlit as st

from utils import data_loader as dl
from utils import state
from utils.error_handler import notify_success, safe
from utils.theme import kpi_card, page_header, section_title

SAMPLE_PATH = os.path.join("data", "covid19_clinical_dataset.csv")


@safe
def render() -> None:
    page_header("Importation des donnees",
                "Chargez votre fichier CSV ou utilisez le dataset d'exemple.")

    col_up, col_sample = st.columns([2, 1])
    with col_up:
        fichier = st.file_uploader("Fichier CSV", type=["csv"])
    with col_sample:
        st.write("")
        st.write("")
        if st.button("Charger le dataset COVID-19 d'exemple",
                     width='stretch'):
            if os.path.exists(SAMPLE_PATH):
                df = dl.load_csv(SAMPLE_PATH)
                _ingest(df, os.path.basename(SAMPLE_PATH))
            else:
                st.error("Le fichier d'exemple est introuvable dans data/.")

    if fichier is not None:
        df = dl.load_csv(fichier)
        _ingest(df, fichier.name)

    df = st.session_state.get("df")
    if df is None:
        st.info("Aucune donnee chargee pour l'instant.")
        return

    _show_overview(df)


def _ingest(df: pd.DataFrame, name: str) -> None:
    """Enregistre le dataset avec une barre de progression (chargement dynamique)."""
    barre = st.progress(0, text="Lecture du fichier...")
    for i, txt in [(35, "Analyse des colonnes..."),
                   (70, "Calcul des metriques..."),
                   (100, "Termine")]:
        time.sleep(0.15)
        barre.progress(i, text=txt)
    state.set_data(df, name)
    barre.empty()
    notify_success(f"Fichier « {name} » importe avec succes.")


def _show_overview(df: pd.DataFrame) -> None:
    ov = dl.dataset_overview(df)

    section_title("Indicateurs cles")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Lignes", f"{ov['lignes']:,}".replace(",", " "))
    with c2:
        kpi_card("Colonnes", ov["colonnes"])
    with c3:
        kpi_card("Doublons", ov["doublons"])
    with c4:
        kpi_card("Memoire", f"{ov['memoire_mo']} Mo")

    section_title("Apercu du dataset")
    n = st.slider("Nombre de lignes a afficher", 5, 50, 10)
    st.dataframe(df.head(n), width='stretch')

    section_title("Detection automatique des colonnes")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Colonnes numeriques ({ov['n_numeriques']})**")
        st.write(", ".join(ov["numeriques"]) or "_aucune_")
    with c2:
        st.markdown(f"**Colonnes categorielles ({ov['n_categorielles']})**")
        st.write(", ".join(ov["categorielles"]) or "_aucune_")
    if ov["temporelles"]:
        st.markdown(f"**Colonnes temporelles :** {', '.join(ov['temporelles'])}")

    section_title("Types des colonnes")
    st.dataframe(dl.info_table(df), width='stretch', hide_index=True)

    section_title("Statistiques descriptives")
    st.dataframe(df.describe(include="all").T, width='stretch')

    with st.expander("Informations generales (df.info)"):
        st.code(dl.info_text(df))
