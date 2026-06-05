"""
app.py  ->  Point d'entree de l'application
===========================================
Tableau de bord medical : analyse des donnees COVID-19.

Conception : interface moderne, minimaliste et epuree, sans emoji, avec une
palette calme (teal / bleu doux / gris clairs / blancs).

Fonctions principales (conformes a l'architecture demandee) :
    - initialiser_etat()          : initialise l'etat de session
    - charger_style_css()         : injecte le theme (importee de utils.theme)
    - afficher_side_navigation()  : construit la barre laterale
    - afficher_tableau_de_bord()  : affiche le tableau de bord (page Accueil)

Auteur : Saad Elidrissi El Hassan
Lancement : streamlit run app.py
"""

from __future__ import annotations

import os
import sys

# Le dossier pages/ porte le meme nom que la convention multipage de Streamlit.
# On ajoute la racine du projet au PYTHONPATH pour garantir l'import des
# packages locaux (pages, utils) quel que soit le mode d'execution.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# Pages
from pages import apropos, exploration, exportation, home
from pages import importation, preprocessing as page_prep, visualisation
# Utilitaires
from utils import state
from utils.theme import charger_style_css

# ---------------------------------------------------------------------
# Configuration generale de la page
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Tableau de bord COVID-19",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Table de routage : libelle -> fonction de rendu
PAGES = {
    "Accueil": home.render,
    "Importation des donnees": importation.render,
    "Analyse exploratoire": exploration.render,
    "Preprocessing": page_prep.render,
    "Visualisations": visualisation.render,
    "Exportation": exportation.render,
    "A propos": apropos.render,
}


def initialiser_etat() -> None:
    """Initialise l'etat de session et applique le theme (CSS)."""
    state.init_state()
    charger_style_css()


def _basculer_theme() -> None:
    """Callback du selecteur de theme.

    Le widget « Mode sombre » est lie a st.session_state['dark_mode'] via sa
    cle. Lorsqu'il change, Streamlit relance le script : charger_style_css()
    reinjecte alors automatiquement la bonne feuille de style. Ce callback sert
    a journaliser le changement de maniere non disruptive.
    """
    mode = "sombre" if st.session_state.get("dark_mode") else "clair"
    state.log_action(f"Changement de theme -> mode {mode}")


def afficher_side_navigation() -> str:
    """Construit la barre laterale (navigation + filtres) et renvoie la page.

    Utilise st.session_state (cle 'nav') pour memoriser la page courante et un
    callback on_change pour le selecteur de theme.
    """
    with st.sidebar:
        st.markdown('<div class="brand">Suivi COVID-19</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Sciences de donnees medicales</div>',
                    unsafe_allow_html=True)
        st.divider()

        # Navigation memorisee dans la session
        choix = st.radio("Navigation", list(PAGES.keys()),
                         key="nav", label_visibility="collapsed")

        st.divider()

        # Selecteur de theme : lie a session_state via la cle, callback on_change
        st.toggle("Mode sombre", key="dark_mode", on_change=_basculer_theme)

        st.divider()

        # Etat du dataset
        if st.session_state.get("df") is not None:
            df = st.session_state.df
            st.markdown("**Jeu de donnees**")
            st.caption(f"{st.session_state.filename}")
            st.caption(f"{df.shape[0]} lignes  -  {df.shape[1]} colonnes")
        else:
            st.info("Aucun jeu de donnees charge.")

        # Historique des traitements
        with st.expander("Historique des traitements"):
            hist = state.get_history_df()
            if hist.empty:
                st.caption("Aucune action pour le moment.")
            else:
                st.dataframe(hist, width='stretch', hide_index=True)

        st.divider()
        st.caption("Saad Elidrissi El Hassan - 2026")

    return choix


def main() -> None:
    """Boucle principale : etat, navigation, puis rendu de la page choisie."""
    initialiser_etat()
    page = afficher_side_navigation()
    PAGES[page]()


if __name__ == "__main__":
    main()
