"""
utils/data_loader.py
--------------------
Importation et inspection des donnees.

Fonctions :
    - load_csv          : lecture robuste d'un fichier CSV (detection du
      separateur, gestion des dates),
    - dataset_overview  : dictionnaire de metriques generales (dimensions,
      memoire, doublons, colonnes num/cat),
    - dtypes_table      : table des types de colonnes,
    - info_table        : equivalent de df.info() sous forme de tableau,
    - detect_columns    : separation colonnes numeriques / categorielles.

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

import io
from typing import Dict, List, Tuple

import pandas as pd


def load_csv(file) -> pd.DataFrame:
    """Charge un CSV de maniere robuste.

    - Detecte automatiquement le separateur (`sep=None` + moteur python).
    - Tente de convertir les colonnes ressemblant a des dates.
    """
    df = pd.read_csv(file, sep=None, engine="python")
    # Tentative de conversion des colonnes de type date
    for col in df.columns:
        if df[col].dtype == "object" and "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except Exception:  # noqa: BLE001
                pass
    return df


def detect_columns(df: pd.DataFrame) -> Tuple[List[str], List[str], List[str]]:
    """Detecte les colonnes numeriques, categorielles et temporelles."""
    numeriques = df.select_dtypes(include="number").columns.tolist()
    temporelles = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    categorielles = [
        c for c in df.columns if c not in numeriques and c not in temporelles
    ]
    return numeriques, categorielles, temporelles


def dataset_overview(df: pd.DataFrame) -> Dict[str, object]:
    """Calcule les principales metriques generales du dataset."""
    numeriques, categorielles, temporelles = detect_columns(df)
    memoire = df.memory_usage(deep=True).sum() / 1024 ** 2  # Mo
    manquantes = int(df.isna().sum().sum())
    cellules = df.shape[0] * df.shape[1]
    return {
        "lignes": df.shape[0],
        "colonnes": df.shape[1],
        "numeriques": numeriques,
        "categorielles": categorielles,
        "temporelles": temporelles,
        "n_numeriques": len(numeriques),
        "n_categorielles": len(categorielles),
        "doublons": int(df.duplicated().sum()),
        "manquantes": manquantes,
        "pct_manquantes": round(100 * manquantes / cellules, 2) if cellules else 0,
        "memoire_mo": round(memoire, 3),
    }


def dtypes_table(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne une table colonne -> type."""
    return (
        df.dtypes.astype(str)
        .reset_index()
        .rename(columns={"index": "Colonne", 0: "Type"})
    )


def info_table(df: pd.DataFrame) -> pd.DataFrame:
    """Reconstruit les informations de df.info() sous forme de tableau."""
    return pd.DataFrame({
        "Colonne": df.columns,
        "Non-Null": df.notna().sum().values,
        "Null": df.isna().sum().values,
        "% Null": (100 * df.isna().mean()).round(2).values,
        "Type": df.dtypes.astype(str).values,
        "Valeurs uniques": [df[c].nunique() for c in df.columns],
    })


def info_text(df: pd.DataFrame) -> str:
    """Retourne la sortie texte brute de df.info() (pour affichage/export)."""
    buf = io.StringIO()
    df.info(buf=buf)
    return buf.getvalue()
