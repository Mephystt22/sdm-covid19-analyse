"""
utils/export.py
---------------
Exportation des resultats.

Fournit des fonctions qui retournent des objets `bytes` prets a etre passes
a `st.download_button` :
    - to_csv_bytes      : dataset nettoye en CSV,
    - to_excel_bytes    : dataset nettoye en Excel (moteur openpyxl),
    - fig_to_png_bytes  : figure Matplotlib en PNG,
    - plotly_to_png/html: figure Plotly en PNG (si kaleido) sinon HTML,
    - build_report      : rapport d'analyse texte/Markdown.

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

import io
from datetime import datetime

import pandas as pd


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convertit un DataFrame en CSV (bytes UTF-8)."""
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame, sheet_name: str = "donnees") -> bytes:
    """Convertit un DataFrame en fichier Excel (.xlsx) via openpyxl."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    buffer.seek(0)
    return buffer.getvalue()


def stats_to_csv_bytes(stats: pd.DataFrame) -> bytes:
    """Exporte la table de statistiques descriptives en CSV."""
    return stats.to_csv().encode("utf-8")


def fig_to_png_bytes(fig) -> bytes:
    """Convertit une figure Matplotlib en PNG (bytes)."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    buffer.seek(0)
    return buffer.getvalue()


def plotly_to_bytes(fig) -> tuple[bytes, str]:
    """Exporte une figure Plotly.

    Retourne (contenu, extension). Tente le PNG via kaleido ; en cas
    d'absence de kaleido, bascule sur un export HTML interactif.
    """
    try:
        return fig.to_image(format="png", scale=2), "png"
    except Exception:  # noqa: BLE001 (kaleido absent)
        html = fig.to_html(include_plotlyjs="cdn").encode("utf-8")
        return html, "html"


def build_report(filename: str, overview: dict, stats: pd.DataFrame,
                 missing: pd.DataFrame, history: list) -> bytes:
    """Genere un rapport d'analyse au format Markdown (bytes)."""
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    lignes = [
        "# Rapport d'analyse - Sciences de Donnees Medicales (COVID-19)",
        "",
        "**Auteur :** Saad Elidrissi El Hassan  ",
        f"**Date :** {now}  ",
        f"**Fichier analyse :** {filename}",
        "",
        "## 1. Apercu general du dataset",
        "",
        f"- Nombre de lignes : **{overview['lignes']}**",
        f"- Nombre de colonnes : **{overview['colonnes']}**",
        f"- Colonnes numeriques : **{overview['n_numeriques']}**",
        f"- Colonnes categorielles : **{overview['n_categorielles']}**",
        f"- Doublons : **{overview['doublons']}**",
        f"- Valeurs manquantes : **{overview['manquantes']}** "
        f"({overview['pct_manquantes']} %)",
        f"- Memoire utilisee : **{overview['memoire_mo']} Mo**",
        "",
        "## 2. Statistiques descriptives",
        "",
        stats.to_markdown() if not stats.empty else "_Aucune variable numerique._",
        "",
        "## 3. Valeurs manquantes par colonne",
        "",
        missing.to_markdown(index=False),
        "",
        "## 4. Historique des traitements appliques",
        "",
    ]
    if history:
        for h in history:
            lignes.append(f"- `{h['heure']}` - {h['action']}")
    else:
        lignes.append("_Aucun traitement applique._")

    lignes += [
        "",
        "---",
        "_Rapport genere automatiquement par l'application SDM COVID-19._",
    ]
    return "\n".join(lignes).encode("utf-8")
