"""
pages/exploration.py  ->  Page "Analyse exploratoire"
-----------------------------------------------------
Analyse exploratoire complete organisee en onglets :
    1. Statistiques (moyenne, mediane, mode, variance, ecart-type,
       min, max, quartiles)
    2. Correlations (matrice + heatmap interactive)
    3. Distributions (histogrammes, boxplots, densite, scatter, pie, bar)
    4. Valeurs manquantes (table, %, visualisation)
    5. Doublons (nombre + lignes dupliquees)
"""

from __future__ import annotations

import streamlit as st

from utils import data_loader as dl
from utils import statistics as stt
from utils import visualization as viz
from utils.error_handler import require_data, safe
from utils.theme import kpi_card, page_header, section_title


@safe
@require_data
def render() -> None:
    df = st.session_state.df
    page_header("Analyse exploratoire des donnees",
                "Comprendre la structure et les caracteristiques du dataset.")

    num, cat, temp = dl.detect_columns(df)

    onglets = st.tabs([
        "Statistiques", "Correlations", "Distributions",
        "Valeurs manquantes", "Doublons",
    ])

    # --- 1. Statistiques ---
    with onglets[0]:
        section_title("Statistiques descriptives completes")
        stats = stt.describe_full(df)
        if stats.empty:
            st.info("Aucune variable numerique disponible.")
        else:
            st.dataframe(stats, width='stretch')
        if cat:
            section_title("Repartition d'une variable categorielle")
            choix = st.selectbox("Variable categorielle", cat, key="eda_cat")
            st.dataframe(stt.categorical_summary(df, choix),
                         width='stretch', hide_index=True)

    # --- 2. Correlations ---
    with onglets[1]:
        section_title("Matrice de correlation")
        methode = st.radio("Methode", ["pearson", "spearman"],
                           horizontal=True, key="corr_method")
        corr = stt.correlation_matrix(df, method=methode)
        if corr.empty:
            st.info("Il faut au moins deux variables numeriques.")
        else:
            st.plotly_chart(viz.heatmap_corr(corr), width='stretch')
            with st.expander("Voir la matrice (valeurs)"):
                st.dataframe(corr, width='stretch')

    # --- 3. Distributions ---
    with onglets[2]:
        section_title("Analyse des distributions")
        type_g = st.selectbox(
            "Type de graphique",
            ["Histogramme", "Boxplot", "Densite", "Nuage de points",
             "Diagramme circulaire", "Diagramme en barres"],
        )
        if type_g in ("Histogramme", "Boxplot", "Densite"):
            if not num:
                st.info("Aucune variable numerique.")
            else:
                col = st.selectbox("Variable numerique", num, key="dist_num")
                grp = st.selectbox("Grouper par (optionnel)", ["(aucun)"] + cat,
                                   key="dist_grp")
                grp = None if grp == "(aucun)" else grp
                if type_g == "Histogramme":
                    st.plotly_chart(viz.histogram(df, col, color=grp),
                                    width='stretch')
                elif type_g == "Boxplot":
                    st.plotly_chart(viz.boxplot(df, col, group=grp),
                                    width='stretch')
                else:
                    st.plotly_chart(viz.density(df, col, group=grp),
                                    width='stretch')
        elif type_g == "Nuage de points":
            if len(num) < 2:
                st.info("Il faut au moins deux variables numeriques.")
            else:
                x = st.selectbox("Axe X", num, key="sc_x")
                y = st.selectbox("Axe Y", num, index=1, key="sc_y")
                color = st.selectbox("Couleur (optionnel)", ["(aucun)"] + cat,
                                     key="sc_c")
                color = None if color == "(aucun)" else color
                st.plotly_chart(viz.scatter(df, x, y, color=color),
                                width='stretch')
        else:  # pie / bar
            if not cat:
                st.info("Aucune variable categorielle.")
            else:
                col = st.selectbox("Variable categorielle", cat, key="pb_col")
                if type_g == "Diagramme circulaire":
                    st.plotly_chart(viz.pie(df, col), width='stretch')
                else:
                    st.plotly_chart(viz.bar(df, col), width='stretch')

    # --- 4. Valeurs manquantes ---
    with onglets[3]:
        section_title("Analyse des valeurs manquantes")
        miss = stt.missing_table(df)
        total = int(df.isna().sum().sum())
        c1, c2 = st.columns(2)
        with c1:
            kpi_card("Total manquantes", total)
        with c2:
            pct = round(100 * total / (df.shape[0] * df.shape[1]), 2)
            kpi_card("Pourcentage global", f"{pct} %")
        st.dataframe(miss, width='stretch', hide_index=True)
        if total > 0:
            st.plotly_chart(viz.missing_bar(miss), width='stretch')
        else:
            st.success("Aucune valeur manquante dans le dataset.")

    # --- 5. Doublons ---
    with onglets[4]:
        section_title("Analyse des doublons")
        ndup = int(df.duplicated().sum())
        kpi_card("Lignes dupliquees", ndup)
        if ndup > 0:
            st.dataframe(stt.duplicate_rows(df), width='stretch')
        else:
            st.success("Aucun doublon detecte.")
