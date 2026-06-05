"""
utils/visualization.py
----------------------
Generation des graphiques avec Plotly (interactif) et Matplotlib (export PNG).

Tous les graphiques adoptent la charte graphique de l'application (palette
calme teal / bleu doux, typographie Inter, fonds transparents) via
`theme.style_fig`, et restent lisibles en mode clair comme en mode sombre.

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

from typing import Optional

import matplotlib
matplotlib.use("Agg")  # backend non interactif (export serveur)
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import CHART_SEQUENCE, palette, style_fig

# Echelle continue calme (teal -> bleu doux) pour les heatmaps thematiques
SOFT_SCALE = [[0.0, "#E8F2F1"], [0.5, "#5FB3B0"], [1.0, "#0E7C7B"]]


# =====================================================================
#  GRAPHIQUES PLOTLY (INTERACTIFS)
# =====================================================================

def histogram(df: pd.DataFrame, col: str, color: Optional[str] = None,
              nbins: int = 30, color_seq: Optional[str] = None) -> go.Figure:
    """Histogramme interactif."""
    fig = px.histogram(df, x=col, color=color, nbins=nbins,
                       color_discrete_sequence=[color_seq] if color_seq else CHART_SEQUENCE,
                       marginal="box")
    fig.update_layout(title=f"Distribution de {col}", bargap=0.06)
    return style_fig(fig)


def boxplot(df: pd.DataFrame, col: str, group: Optional[str] = None) -> go.Figure:
    """Boite a moustaches, eventuellement groupee."""
    fig = px.box(df, y=col, x=group, color=group)
    fig.update_layout(title=f"Boxplot de {col}")
    return style_fig(fig)


def density(df: pd.DataFrame, col: str, group: Optional[str] = None) -> go.Figure:
    """Courbe de densite (violon + boite)."""
    fig = px.violin(df, y=col, x=group, color=group, box=True, points=False)
    fig.update_layout(title=f"Densite de {col}")
    return style_fig(fig)


def scatter(df: pd.DataFrame, x: str, y: str, color: Optional[str] = None,
            size: Optional[str] = None) -> go.Figure:
    """Nuage de points."""
    fig = px.scatter(df, x=x, y=y, color=color, size=size, opacity=0.75)
    fig.update_layout(title=f"{y} en fonction de {x}")
    return style_fig(fig)


def pie(df: pd.DataFrame, col: str) -> go.Figure:
    """Diagramme circulaire d'une variable categorielle."""
    vc = df[col].value_counts().reset_index()
    vc.columns = [col, "count"]
    fig = px.pie(vc, names=col, values="count", hole=0.45,
                 color_discrete_sequence=CHART_SEQUENCE)
    fig.update_layout(title=f"Repartition de {col}")
    return style_fig(fig)


def bar(df: pd.DataFrame, col: str, color_seq: Optional[str] = None) -> go.Figure:
    """Diagramme en barres des effectifs d'une variable categorielle."""
    vc = df[col].value_counts().reset_index()
    vc.columns = [col, "count"]
    fig = px.bar(vc, x=col, y="count",
                 color_discrete_sequence=[color_seq] if color_seq else CHART_SEQUENCE)
    fig.update_layout(title=f"Effectifs de {col}")
    return style_fig(fig)


def heatmap_corr(corr: pd.DataFrame) -> go.Figure:
    """Heatmap interactive d'une matrice de correlation."""
    fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                    color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    fig.update_layout(title="Matrice de correlation")
    return style_fig(fig)


def missing_bar(missing_df: pd.DataFrame) -> go.Figure:
    """Visualisation des valeurs manquantes (barres horizontales)."""
    data = missing_df[missing_df["% Manquantes"] > 0]
    fig = px.bar(data, x="% Manquantes", y="Colonne", orientation="h",
                 color="% Manquantes", color_continuous_scale=SOFT_SCALE)
    fig.update_layout(title="Pourcentage de valeurs manquantes par colonne")
    return style_fig(fig)


def time_series(df: pd.DataFrame, date_col: str, value_col: str,
                agg: str = "count") -> go.Figure:
    """Graphique temporel : agregation hebdomadaire d'une valeur par date."""
    tmp = df[[date_col, value_col]].dropna().copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
    tmp = tmp.dropna(subset=[date_col])
    grp = tmp.groupby(pd.Grouper(key=date_col, freq="W"))[value_col]
    serie = (grp.count() if agg == "count" else grp.mean()).reset_index()
    fig = px.line(serie, x=date_col, y=value_col, markers=True)
    fig.update_traces(line_color="#0E7C7B")
    fig.update_layout(title=f"Evolution temporelle ({agg}) de {value_col}")
    return style_fig(fig)


def comparison_bar(df: pd.DataFrame, cat: str, num: str,
                   agg: str = "mean") -> go.Figure:
    """Graphique comparatif : statistique d'une variable numerique par categorie."""
    grp = df.groupby(cat)[num]
    serie = (grp.mean() if agg == "mean" else grp.sum()).reset_index()
    fig = px.bar(serie, x=cat, y=num, color=cat,
                 color_discrete_sequence=CHART_SEQUENCE)
    fig.update_layout(title=f"{agg} de {num} par {cat}", showlegend=False)
    return style_fig(fig)


# =====================================================================
#  GRAPHIQUES MATPLOTLIB (EXPORT PNG)
# =====================================================================

def mpl_histogram(df: pd.DataFrame, col: str):
    """Histogramme Matplotlib (figure exportable en PNG)."""
    c = palette()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(df[col].dropna(), bins=30, color="#0E7C7B", edgecolor="white")
    ax.set_title(f"Distribution de {col}", color=c["text"])
    ax.set_xlabel(col)
    ax.set_ylabel("Frequence")
    fig.patch.set_alpha(0)
    fig.tight_layout()
    return fig


def mpl_corr_heatmap(corr: pd.DataFrame):
    """Heatmap de correlation Matplotlib (export PNG)."""
    fig, ax = plt.subplots(figsize=(8, 6.5))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90, fontsize=7)
    ax.set_yticklabels(corr.columns, fontsize=7)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Matrice de correlation")
    fig.tight_layout()
    return fig
