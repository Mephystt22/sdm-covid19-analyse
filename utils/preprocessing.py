"""
utils/preprocessing.py
----------------------
Nettoyage et transformation des donnees.

Couvre :
    - Gestion des valeurs manquantes (suppression, moyenne, mediane, mode,
      valeur personnalisee),
    - Gestion des doublons,
    - Detection et suppression des outliers (IQR / Z-score),
    - Transformations : normalisation (Min-Max), standardisation (Z-score),
      encodage des variables categorielles (label / one-hot),
    - Renommage de colonnes, changement de type,
    - Selection / suppression de colonnes,
    - Filtrage, recherche et tri.

Toutes les fonctions retournent une COPIE du DataFrame (immuabilite).

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

# =====================================================================
#  VALEURS MANQUANTES
# =====================================================================

def drop_missing_rows(df: pd.DataFrame, subset: List[str] | None = None) -> pd.DataFrame:
    """Supprime les lignes contenant des valeurs manquantes."""
    return df.dropna(subset=subset).reset_index(drop=True)


def drop_missing_cols(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Supprime les colonnes dont la proportion de NaN depasse `threshold`."""
    limite = int((1 - threshold) * len(df))
    return df.dropna(axis=1, thresh=limite)


def fill_missing(df: pd.DataFrame, cols: List[str], strategy: str,
                 custom_value=None) -> pd.DataFrame:
    """Remplit les valeurs manquantes selon une strategie.

    strategy : 'mean' | 'median' | 'mode' | 'custom'
    """
    out = df.copy()
    for col in cols:
        if strategy == "mean":
            out[col] = out[col].fillna(out[col].mean())
        elif strategy == "median":
            out[col] = out[col].fillna(out[col].median())
        elif strategy == "mode":
            mode = out[col].mode(dropna=True)
            if not mode.empty:
                out[col] = out[col].fillna(mode.iloc[0])
        elif strategy == "custom":
            out[col] = out[col].fillna(custom_value)
    return out


# =====================================================================
#  DOUBLONS
# =====================================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime automatiquement les lignes dupliquees."""
    return df.drop_duplicates().reset_index(drop=True)


# =====================================================================
#  OUTLIERS (VALEURS ABERRANTES)
# =====================================================================

def detect_outliers_iqr(df: pd.DataFrame, col: str, k: float = 1.5):
    """Detecte les outliers d'une colonne via la methode de l'IQR.

    Retourne (masque_outliers, borne_basse, borne_haute).
    """
    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr = q3 - q1
    basse, haute = q1 - k * iqr, q3 + k * iqr
    mask = (df[col] < basse) | (df[col] > haute)
    return mask, basse, haute


def detect_outliers_zscore(df: pd.DataFrame, col: str, seuil: float = 3.0):
    """Detecte les outliers via le Z-score (|z| > seuil)."""
    serie = df[col]
    z = (serie - serie.mean()) / serie.std(ddof=0)
    return z.abs() > seuil


def remove_outliers(df: pd.DataFrame, col: str, method: str = "iqr",
                    k: float = 1.5, seuil: float = 3.0) -> pd.DataFrame:
    """Supprime les lignes outliers d'une colonne."""
    if method == "iqr":
        mask, _, _ = detect_outliers_iqr(df, col, k)
    else:
        mask = detect_outliers_zscore(df, col, seuil)
    return df[~mask].reset_index(drop=True)


# =====================================================================
#  TRANSFORMATIONS NUMERIQUES
# =====================================================================

def normalize(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Normalisation Min-Max -> valeurs ramenees dans [0, 1]."""
    out = df.copy()
    for col in cols:
        mn, mx = out[col].min(), out[col].max()
        if mx != mn:
            out[col] = (out[col] - mn) / (mx - mn)
    return out


def standardize(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Standardisation Z-score -> moyenne 0, ecart-type 1."""
    out = df.copy()
    for col in cols:
        mu, sigma = out[col].mean(), out[col].std()
        if sigma != 0:
            out[col] = (out[col] - mu) / sigma
    return out


# =====================================================================
#  ENCODAGE DES VARIABLES CATEGORIELLES
# =====================================================================

def encode_label(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Encodage par etiquette (chaque modalite -> entier)."""
    out = df.copy()
    for col in cols:
        out[col] = out[col].astype("category").cat.codes
    return out


def encode_onehot(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Encodage one-hot (variables indicatrices)."""
    return pd.get_dummies(df, columns=cols)


# =====================================================================
#  RENOMMAGE / TYPES / SELECTION DE COLONNES
# =====================================================================

def rename_column(df: pd.DataFrame, old: str, new: str) -> pd.DataFrame:
    """Renomme une colonne."""
    return df.rename(columns={old: new})


def change_dtype(df: pd.DataFrame, col: str, new_type: str) -> pd.DataFrame:
    """Change le type d'une colonne.

    new_type : 'int' | 'float' | 'str' | 'category' | 'datetime'
    """
    out = df.copy()
    if new_type == "int":
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64")
    elif new_type == "float":
        out[col] = pd.to_numeric(out[col], errors="coerce").astype(float)
    elif new_type == "str":
        out[col] = out[col].astype(str)
    elif new_type == "category":
        out[col] = out[col].astype("category")
    elif new_type == "datetime":
        out[col] = pd.to_datetime(out[col], errors="coerce")
    return out


def drop_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Supprime une liste de colonnes."""
    return df.drop(columns=cols)


def select_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Ne conserve que les colonnes utiles selectionnees."""
    return df[cols].copy()


# =====================================================================
#  FILTRAGE / RECHERCHE / TRI
# =====================================================================

def filter_numeric(df: pd.DataFrame, col: str, mn: float, mx: float) -> pd.DataFrame:
    """Filtre dynamique sur une plage de valeurs numeriques."""
    return df[(df[col] >= mn) & (df[col] <= mx)]


def filter_categorical(df: pd.DataFrame, col: str, values: List[str]) -> pd.DataFrame:
    """Filtre sur une liste de modalites selectionnees."""
    return df[df[col].astype(str).isin(values)]


def search_text(df: pd.DataFrame, col: str, query: str) -> pd.DataFrame:
    """Recherche textuelle (insensible a la casse) dans une colonne."""
    return df[df[col].astype(str).str.contains(query, case=False, na=False)]


def sort_values(df: pd.DataFrame, col: str, ascending: bool = True) -> pd.DataFrame:
    """Tri ascendant ou descendant selon une colonne."""
    return df.sort_values(col, ascending=ascending).reset_index(drop=True)
