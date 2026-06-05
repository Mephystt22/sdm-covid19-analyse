"""
pages/home.py  ->  Page "Accueil"
---------------------------------
Page d'accueil avec presentation de l'application et, lorsqu'un jeu de donnees
est charge, un tableau de bord analytique (KPI cards + apercus).

La fonction afficher_tableau_de_bord() concentre la logique du tableau de bord.
"""

from __future__ import annotations

import streamlit as st

from utils import data_loader as dl
from utils import statistics as stt
from utils import visualization as viz
from utils.theme import kpi_card, page_header, section_title


def afficher_tableau_de_bord(df) -> None:
    """Affiche le tableau de bord analytique pour le jeu de donnees charge."""
    ov = dl.dataset_overview(df)

    section_title("Indicateurs cles")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Lignes", f"{ov['lignes']:,}".replace(",", " "))
    with c2:
        kpi_card("Colonnes", ov["colonnes"])
    with c3:
        kpi_card("Valeurs manquantes", f"{ov['pct_manquantes']} %")
    with c4:
        kpi_card("Doublons", ov["doublons"])

    st.write("")
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        kpi_card("Numeriques / Categorielles",
                 f"{ov['n_numeriques']} / {ov['n_categorielles']}")
    with c6:
        kpi_card("Memoire", f"{ov['memoire_mo']} Mo")
    with c7:
        kpi_card("Fichier", st.session_state.get("filename", "-"))
    with c8:
        kpi_card("Traitements appliques", len(st.session_state.get("history", [])))

    st.write("")
    section_title("Apercus")
    g1, g2 = st.columns(2)
    with g1:
        corr = stt.correlation_matrix(df)
        if not corr.empty:
            st.plotly_chart(viz.heatmap_corr(corr), width='stretch')
        else:
            st.info("Pas assez de variables numeriques pour la correlation.")
    with g2:
        cats = ov["categorielles"]
        if cats:
            st.plotly_chart(viz.pie(df, cats[0]), width='stretch')
        elif ov["numeriques"]:
            st.plotly_chart(viz.histogram(df, ov["numeriques"][0]), width='stretch')


def render() -> None:
    page_header(
        "Tableau de bord - Donnees COVID-19",
        "Analyse exploratoire, nettoyage, preprocessing et visualisation "
        "de donnees cliniques.",
    )

    df = st.session_state.get("df")

    if df is None:
        st.info(
            "Bienvenue. Cette plateforme permet d'importer, d'explorer, de "
            "nettoyer et de visualiser des donnees medicales. Commencez par la "
            "page Importation des donnees dans la barre laterale, ou chargez le "
            "jeu de donnees COVID-19 d'exemple."
        )

        section_title("Fonctionnalites principales")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Importer**  \nCharger un fichier CSV et inspecter "
                        "automatiquement sa structure.")
            st.markdown("**Explorer**  \nStatistiques, correlations, "
                        "distributions, valeurs manquantes.")
        with c2:
            st.markdown("**Nettoyer**  \nValeurs manquantes, doublons, "
                        "outliers, transformations.")
            st.markdown("**Visualiser**  \nGraphiques interactifs "
                        "personnalisables et exportables.")
        with c3:
            st.markdown("**Exporter**  \nDonnees nettoyees (CSV / Excel), "
                        "graphiques (PNG), rapport d'analyse.")
            st.markdown("**Options avancees**  \nMode sombre, historique, "
                        "comparaison avant / apres.")
        return

    afficher_tableau_de_bord(df)
