"""
utils/state.py
--------------
Initialisation et gestion de l'etat global de l'application via
`st.session_state`.

Gere notamment :
    - le dataset courant (`df`) et le dataset original (`df_original`),
    - l'historique des traitements appliques,
    - la sauvegarde automatique d'instantanes (autosave),
    - l'apercu avant/apres nettoyage.

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

import datetime as _dt
from typing import Optional

import pandas as pd
import streamlit as st

# Valeurs par defaut de l'etat de session
_DEFAULTS = {
    "df": None,                 # dataset courant (modifie par le preprocessing)
    "df_original": None,        # copie immuable du dataset importe
    "filename": None,           # nom du fichier importe
    "history": [],              # liste des operations realisees
    "snapshots": [],            # instantanes pour comparaison/annulation
    "dark_mode": False,         # mode sombre actif ?
}


def init_state() -> None:
    """Initialise les cles de session manquantes (idempotent)."""
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_data(df: pd.DataFrame, filename: str) -> None:
    """Enregistre un nouveau dataset importe et reinitialise l'historique."""
    st.session_state.df = df.copy()
    st.session_state.df_original = df.copy()
    st.session_state.filename = filename
    st.session_state.history = []
    st.session_state.snapshots = [("Import initial", df.copy())]
    log_action(f"Importation du fichier « {filename} » "
               f"({df.shape[0]} lignes, {df.shape[1]} colonnes)")


def get_data() -> Optional[pd.DataFrame]:
    """Retourne le dataset courant (ou None)."""
    return st.session_state.get("df")


def update_data(df: pd.DataFrame, action: str, autosave: bool = True) -> None:
    """Met a jour le dataset courant et journalise l'action.

    Si `autosave` est actif, un instantane est conserve pour permettre la
    comparaison avant/apres et l'annulation.
    """
    if autosave:
        st.session_state.snapshots.append((action, df.copy()))
        # On limite l'historique des instantanes a 20 pour la memoire
        st.session_state.snapshots = st.session_state.snapshots[-20:]
    st.session_state.df = df
    log_action(action)


def log_action(action: str) -> None:
    """Ajoute une entree horodatee a l'historique des traitements."""
    horodatage = _dt.datetime.now().strftime("%H:%M:%S")
    st.session_state.history.append({"heure": horodatage, "action": action})


def reset_to_original() -> None:
    """Restaure le dataset original (annule tous les traitements)."""
    if st.session_state.df_original is not None:
        st.session_state.df = st.session_state.df_original.copy()
        log_action("Reinitialisation : retour au dataset original")


def get_history_df() -> pd.DataFrame:
    """Retourne l'historique sous forme de DataFrame affichable."""
    if not st.session_state.history:
        return pd.DataFrame(columns=["heure", "action"])
    return pd.DataFrame(st.session_state.history)
