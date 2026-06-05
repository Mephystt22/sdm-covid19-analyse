"""
utils/statistics.py
-------------------
Analyses statistiques et exploratoires.

Fonctions :
    - describe_full      : statistiques completes (moyenne, mediane, mode,
      variance, ecart-type, min, max, quartiles),
    - correlation_matrix : matrice de correlation des variables numeriques,
    - missing_table      : table + pourcentage des valeurs manquantes,
    - duplicate_rows     : lignes dupliquees.

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def describe_full(df: pd.DataFrame) -> pd.DataFrame:
    """Statistiques descriptives completes pour les colonnes numeriques.

    Inclut moyenne, mediane, mode, variance, ecart-type, min, max et
    quartiles (Q1, Q3).
    """
    num = df.select_dtypes(include="number")
    if num.empty:
        return pd.DataFrame()

    stats = pd.DataFrame({
        "Moyenne": num.mean(),
        "Mediane": num.median(),
        "Mode": num.mode(dropna=True).iloc[0] if not num.mode().empty else np.nan,
        "Variance": num.var(),
        "Ecart-type": num.std(),
        "Minimum": num.min(),
        "Q1 (25%)": num.quantile(0.25),
        "Q3 (75%)": num.quantile(0.75),
        "Maximum": num.max(),
    })
    return stats.round(3)


def correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Matrice de correlation des variables numeriques."""
    num = df.select_dtypes(include="number")
    if num.shape[1] < 2:
        return pd.DataFrame()
    return num.corr(method=method).round(3)


def missing_table(df: pd.DataFrame) -> pd.DataFrame:
    """Table des valeurs manquantes par colonne, triee par pourcentage."""
    manquantes = df.isna().sum()
    pct = (100 * df.isna().mean()).round(2)
    table = pd.DataFrame({
        "Colonne": df.columns,
        "Valeurs manquantes": manquantes.values,
        "% Manquantes": pct.values,
    })
    return table.sort_values("% Manquantes", ascending=False).reset_index(drop=True)


def duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne l'ensemble des lignes dupliquees (toutes occurrences)."""
    return df[df.duplicated(keep=False)].sort_values(list(df.columns))


def categorical_summary(df: pd.DataFrame, col: str, top: int = 10) -> pd.DataFrame:
    """Repartition des modalites d'une variable categorielle."""
    vc = df[col].value_counts(dropna=False).head(top)
    return pd.DataFrame({
        col: vc.index.astype(str),
        "Effectif": vc.values,
        "%": (100 * vc.values / len(df)).round(2),
    })
