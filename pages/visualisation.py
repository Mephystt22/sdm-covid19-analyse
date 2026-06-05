"""
pages/visualisation.py  ->  Page "Visualisations"
-------------------------------------------------
Section graphique interactive : histogrammes, boxplots, heatmaps, correlation,
graphiques temporels, nuages de points et graphiques comparatifs.

Personnalisation : choix des colonnes, des couleurs, du nombre de classes,
et exportation du graphique genere (PNG/HTML).
"""

from __future__ import annotations

import streamlit as st

from utils import data_loader as dl
from utils import export as exp
from utils import statistics as stt
from utils import visualization as viz
from utils.error_handler import require_data, safe
from utils.theme import page_header, section_title

# Palette calme et apaisante alignee sur la charte medicale de l'application
PALETTE = {
    "Teal": "#0E7C7B", "Bleu doux": "#3E7CB1", "Turquoise": "#14B8A6",
    "Bleu ardoise": "#5B8DC9", "Gris-bleu": "#64748B", "Vert d'eau": "#5FB3B0",
}


@safe
@require_data
def render() -> None:
    df = st.session_state.df
    page_header("Visualisation des donnees",
                "Graphiques interactifs et personnalisables.")

    num, cat, temp = dl.detect_columns(df)

    section_title("Configuration du graphique")
    type_g = st.selectbox(
        "Type de graphique",
        ["Histogramme", "Boxplot", "Heatmap de correlation", "Nuage de points",
         "Graphique temporel", "Graphique comparatif", "Diagramme en barres"],
    )
    couleur = PALETTE[st.selectbox("Couleur principale", list(PALETTE.keys()))]

    fig = None

    if type_g == "Histogramme" and num:
        col = st.selectbox("Variable", num)
        nbins = st.slider("Nombre de classes", 5, 100, 30)
        fig = viz.histogram(df, col, nbins=nbins, color_seq=couleur)

    elif type_g == "Boxplot" and num:
        col = st.selectbox("Variable", num)
        grp = st.selectbox("Grouper par", ["(aucun)"] + cat)
        fig = viz.boxplot(df, col, None if grp == "(aucun)" else grp)

    elif type_g == "Heatmap de correlation":
        corr = stt.correlation_matrix(df)
        if corr.empty:
            st.info("Il faut au moins deux variables numeriques.")
        else:
            fig = viz.heatmap_corr(corr)

    elif type_g == "Nuage de points" and len(num) >= 2:
        x = st.selectbox("Axe X", num, key="vx")
        y = st.selectbox("Axe Y", num, index=1, key="vy")
        color = st.selectbox("Couleur", ["(aucun)"] + cat, key="vc")
        fig = viz.scatter(df, x, y, None if color == "(aucun)" else color)

    elif type_g == "Graphique temporel":
        date_cols = temp + [c for c in df.columns if "date" in c.lower()]
        date_cols = list(dict.fromkeys(date_cols))
        if not date_cols or not num:
            st.info("Une colonne de date et une variable numerique sont requises.")
        else:
            dcol = st.selectbox("Colonne date", date_cols)
            vcol = st.selectbox("Variable", num)
            agg = st.radio("Agregation", ["count", "mean"], horizontal=True)
            fig = viz.time_series(df, dcol, vcol, agg)

    elif type_g == "Graphique comparatif" and cat and num:
        c = st.selectbox("Categorie", cat)
        n = st.selectbox("Variable numerique", num)
        agg = st.radio("Statistique", ["mean", "sum"], horizontal=True)
        fig = viz.comparison_bar(df, c, n, agg)

    elif type_g == "Diagramme en barres" and cat:
        col = st.selectbox("Variable categorielle", cat)
        fig = viz.bar(df, col, color_seq=couleur)

    else:
        st.info("Type de graphique indisponible avec les colonnes actuelles.")

    if fig is not None:
        st.plotly_chart(fig, width='stretch')

        section_title("Exportation du graphique")
        contenu, ext = exp.plotly_to_bytes(fig)
        mime = "image/png" if ext == "png" else "text/html"
        if ext == "html":
            st.caption("Export PNG indisponible (kaleido absent) : export HTML interactif.")
        st.download_button(f" Telecharger le graphique (.{ext})", contenu,
                           file_name=f"graphique.{ext}", mime=mime)
