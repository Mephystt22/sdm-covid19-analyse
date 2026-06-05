"""
pages/exportation.py  ->  Page "Exportation"
--------------------------------------------
Exportation des resultats :
    - dataset nettoye en CSV,
    - dataset nettoye en Excel (openpyxl),
    - graphique genere en PNG,
    - statistiques descriptives,
    - rapport d'analyse (Markdown).

Inclut egalement une comparaison avant/apres (dataset original vs nettoye).
"""

from __future__ import annotations

import streamlit as st

from utils import data_loader as dl
from utils import export as exp
from utils import statistics as stt
from utils import visualization as viz
from utils.error_handler import require_data, safe
from utils.theme import kpi_card, page_header, section_title


@safe
@require_data
def render() -> None:
    df = st.session_state.df
    original = st.session_state.df_original
    filename = st.session_state.get("filename", "dataset.csv")
    base = filename.rsplit(".", 1)[0]

    page_header("Exportation des resultats",
                "Telechargez vos donnees nettoyees, graphiques et rapports.")

    # --- Comparaison avant / apres ---
    section_title("Comparaison avant / apres nettoyage")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Lignes (orig.)", original.shape[0])
    with c2:
        kpi_card("Lignes (actuel)", df.shape[0])
    with c3:
        kpi_card("NaN (orig.)", int(original.isna().sum().sum()))
    with c4:
        kpi_card("NaN (actuel)", int(df.isna().sum().sum()))

    # --- Donnees ---
    section_title("Donnees nettoyees")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("CSV", exp.to_csv_bytes(df),
                           file_name=f"{base}_nettoye.csv", mime="text/csv",
                           width='stretch')
    with c2:
        st.download_button("Excel (.xlsx)", exp.to_excel_bytes(df),
                           file_name=f"{base}_nettoye.xlsx",
                           mime="application/vnd.openxmlformats-officedocument."
                                "spreadsheetml.sheet",
                           width='stretch')

    # --- Statistiques ---
    section_title("Statistiques descriptives")
    stats = stt.describe_full(df)
    if not stats.empty:
        st.dataframe(stats, width='stretch')
        st.download_button("Statistiques (CSV)",
                           exp.stats_to_csv_bytes(stats),
                           file_name=f"{base}_statistiques.csv", mime="text/csv")

    # --- Graphique PNG (Matplotlib) ---
    section_title("Graphique (PNG)")
    num, _, _ = dl.detect_columns(df)
    if num:
        col = st.selectbox("Variable pour l'histogramme", num)
        fig = viz.mpl_histogram(df, col)
        st.pyplot(fig)
        st.download_button("Histogramme (PNG)", exp.fig_to_png_bytes(fig),
                           file_name=f"{base}_{col}_hist.png", mime="image/png")
        corr = stt.correlation_matrix(df)
        if not corr.empty:
            figc = viz.mpl_corr_heatmap(corr)
            st.download_button("Heatmap correlation (PNG)",
                               exp.fig_to_png_bytes(figc),
                               file_name=f"{base}_correlation.png",
                               mime="image/png")

    # --- Rapport ---
    section_title("Rapport d'analyse complet")
    ov = dl.dataset_overview(df)
    miss = stt.missing_table(df)
    rapport = exp.build_report(filename, ov, stats, miss,
                               st.session_state.get("history", []))
    st.download_button("Rapport d'analyse (Markdown)", rapport,
                       file_name=f"{base}_rapport.md", mime="text/markdown",
                       width='stretch')
