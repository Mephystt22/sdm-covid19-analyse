"""
utils/error_handler.py
----------------------
Gestion centralisee des erreurs et des notifications de succes / erreur.

Fournit :
    - un decorateur `safe` qui capture les exceptions et affiche un message
      clair sans faire planter l'application,
    - des helpers de notification (succes, erreur, info, avertissement).

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

import functools
import traceback
from typing import Any, Callable

import streamlit as st


def notify_success(message: str) -> None:
    """Affiche une notification de succes (toast + banniere)."""
    st.toast(message)
    st.success(message)


def notify_error(message: str) -> None:
    """Affiche une notification d'erreur."""
    st.toast(message)
    st.error(message)


def notify_info(message: str) -> None:
    """Affiche une notification d'information."""
    st.info(message)


def notify_warning(message: str) -> None:
    """Affiche un avertissement."""
    st.warning(message)


def safe(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorateur : execute `func` et capture toute exception.

    En cas d'erreur, un message lisible est affiche a l'utilisateur et la
    trace complete est disponible dans un expander (utile pour le debug).
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 (on veut tout capturer ici)
            notify_error(f"Une erreur est survenue : {exc}")
            with st.expander("Details techniques de l'erreur"):
                st.code("".join(traceback.format_exc()))
            return None

    return wrapper


def require_data(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorateur : verifie qu'un dataset est charge avant d'executer la page.

    Si aucune donnee n'est presente dans la session, un message invite
    l'utilisateur a importer un fichier au lieu d'afficher une page vide.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if st.session_state.get("df") is None:
            notify_warning(
                "Aucune donnee n'est chargee. Rendez-vous dans "
                "**Importation des donnees** pour commencer."
            )
            st.stop()
        return func(*args, **kwargs)

    return wrapper
