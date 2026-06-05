"""
pages/preprocessing.py  ->  Page "Preprocessing"
------------------------------------------------
Nettoyage et transformation des donnees, organise en onglets :
    1. Valeurs manquantes
    2. Doublons
    3. Outliers (avec visualisation avant/apres)
    4. Transformations (normalisation, standardisation, encodage, renommage, type)
    5. Colonnes (selection / suppression)
    6. Filtrage / recherche / tri

Chaque action met a jour le dataset courant, journalise l'operation et
permet la comparaison avant/apres.
"""

from __future__ import annotations

import streamlit as st

from utils import data_loader as dl
from utils import preprocessing as prep
from utils import state
from utils import visualization as viz
from utils.error_handler import notify_success, require_data, safe
from utils.theme import kpi_card, page_header, section_title


@safe
@require_data
def render() -> None:
    df = st.session_state.df
    page_header("Preprocessing des donnees",
                "Nettoyez et transformez votre dataset etape par etape.")

    # Barre d'etat + reinitialisation
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        kpi_card("Lignes", df.shape[0])
    with c2:
        kpi_card("Valeurs manquantes", int(df.isna().sum().sum()))
    with c3:
        st.write("")
        if st.button("Reinitialiser au dataset original",
                     width='stretch'):
            state.reset_to_original()
            notify_success("Dataset reinitialise.")
            st.rerun()

    num, cat, _ = dl.detect_columns(df)

    onglets = st.tabs([
        "Valeurs manquantes", "Doublons", "Outliers",
        "Transformations", "Colonnes", "Filtrage",
    ])

    # --- 1. Valeurs manquantes ---
    with onglets[0]:
        section_title("Gestion des valeurs manquantes")
        action = st.radio(
            "Action",
            ["Supprimer les lignes", "Supprimer les colonnes (seuil)",
             "Remplacer par moyenne", "Remplacer par mediane",
             "Remplacer par mode", "Remplacer par valeur personnalisee"],
        )
        if action == "Supprimer les lignes":
            cols = st.multiselect("Restreindre aux colonnes (optionnel)",
                                  df.columns.tolist())
            if st.button("Appliquer", key="m1"):
                new = prep.drop_missing_rows(df, cols or None)
                state.update_data(new, f"Suppression lignes NaN ({cols or 'toutes'})")
                _done()
        elif action == "Supprimer les colonnes (seuil)":
            seuil = st.slider("Seuil de NaN (proportion)", 0.0, 1.0, 0.5, 0.05)
            if st.button("Appliquer", key="m2"):
                new = prep.drop_missing_cols(df, seuil)
                state.update_data(new, f"Suppression colonnes NaN > {seuil:.0%}")
                _done()
        else:
            cols = st.multiselect("Colonnes a traiter", df.columns.tolist())
            custom = None
            if action == "Remplacer par valeur personnalisee":
                custom = st.text_input("Valeur de remplacement", "0")
            strat = {"Remplacer par moyenne": "mean",
                     "Remplacer par mediane": "median",
                     "Remplacer par mode": "mode",
                     "Remplacer par valeur personnalisee": "custom"}[action]
            if st.button("Appliquer", key="m3") and cols:
                new = prep.fill_missing(df, cols, strat, custom)
                state.update_data(new, f"Imputation {strat} sur {cols}")
                _done()

    # --- 2. Doublons ---
    with onglets[1]:
        section_title("Gestion des doublons")
        st.write(f"Doublons detectes : **{int(df.duplicated().sum())}**")
        if st.button("Supprimer automatiquement les doublons"):
            new = prep.remove_duplicates(df)
            state.update_data(new, "Suppression automatique des doublons")
            _done()

    # --- 3. Outliers ---
    with onglets[2]:
        section_title("Detection et suppression des outliers")
        if not num:
            st.info("Aucune variable numerique.")
        else:
            col = st.selectbox("Variable", num, key="out_col")
            method = st.radio("Methode de detection", ["IQR", "Z-score"],
                              horizontal=True)
            if method == "IQR":
                mask, basse, haute = prep.detect_outliers_iqr(df, col)
                st.write(f"Bornes IQR : [{basse:.2f}, {haute:.2f}] - "
                         f"**{int(mask.sum())}** outliers detectes.")
            else:
                mask = prep.detect_outliers_zscore(df, col)
                st.write(f"**{int(mask.sum())}** outliers detectes (|z| > 3).")

            # Visualisation avant
            st.plotly_chart(viz.boxplot(df, col), width='stretch')

            if st.button("Supprimer les outliers de cette colonne"):
                m = "iqr" if method == "IQR" else "zscore"
                new = prep.remove_outliers(df, col, method=m)
                state.update_data(new, f"Suppression outliers ({method}) sur {col}")
                # Visualisation apres
                st.success(f"{df.shape[0] - new.shape[0]} lignes supprimees.")
                st.plotly_chart(viz.boxplot(new, col), width='stretch')
                st.rerun()

    # --- 4. Transformations ---
    with onglets[3]:
        section_title("Transformation des donnees")
        sous = st.selectbox(
            "Operation",
            ["Normalisation (Min-Max)", "Standardisation (Z-score)",
             "Encodage categoriel", "Renommer une colonne",
             "Changer le type d'une colonne"],
        )
        if sous == "Normalisation (Min-Max)":
            cols = st.multiselect("Colonnes numeriques", num, key="n1")
            if st.button("Normaliser") and cols:
                state.update_data(prep.normalize(df, cols),
                                  f"Normalisation Min-Max {cols}")
                _done()
        elif sous == "Standardisation (Z-score)":
            cols = st.multiselect("Colonnes numeriques", num, key="s1")
            if st.button("Standardiser") and cols:
                state.update_data(prep.standardize(df, cols),
                                  f"Standardisation {cols}")
                _done()
        elif sous == "Encodage categoriel":
            cols = st.multiselect("Colonnes categorielles", cat, key="e1")
            mode = st.radio("Type d'encodage", ["Label", "One-Hot"],
                            horizontal=True)
            if st.button("Encoder") and cols:
                new = (prep.encode_label(df, cols) if mode == "Label"
                       else prep.encode_onehot(df, cols))
                state.update_data(new, f"Encodage {mode} {cols}")
                _done()
        elif sous == "Renommer une colonne":
            old = st.selectbox("Colonne", df.columns.tolist(), key="r1")
            new_name = st.text_input("Nouveau nom", old)
            if st.button("Renommer") and new_name:
                state.update_data(prep.rename_column(df, old, new_name),
                                  f"Renommage {old} -> {new_name}")
                _done()
        else:
            col = st.selectbox("Colonne", df.columns.tolist(), key="t1")
            t = st.selectbox("Nouveau type",
                             ["int", "float", "str", "category", "datetime"])
            if st.button("Convertir"):
                state.update_data(prep.change_dtype(df, col, t),
                                  f"Type {col} -> {t}")
                _done()

    # --- 5. Colonnes ---
    with onglets[4]:
        section_title("Selection des colonnes")
        mode = st.radio("Mode", ["Supprimer des colonnes",
                                 "Conserver uniquement certaines colonnes"],
                        horizontal=True)
        cols = st.multiselect("Colonnes", df.columns.tolist(), key="col_sel")
        if st.button("Appliquer", key="colbtn") and cols:
            if mode == "Supprimer des colonnes":
                state.update_data(prep.drop_columns(df, cols),
                                  f"Suppression colonnes {cols}")
            else:
                state.update_data(prep.select_columns(df, cols),
                                  f"Conservation colonnes {cols}")
            _done()

    # --- 6. Filtrage ---
    with onglets[5]:
        section_title("Filtrage, recherche et tri")
        mode = st.radio("Type", ["Filtre numerique", "Filtre categoriel",
                                  "Recherche textuelle", "Tri"], horizontal=True)
        apercu = df
        if mode == "Filtre numerique" and num:
            col = st.selectbox("Colonne", num, key="f1")
            mn, mx = float(df[col].min()), float(df[col].max())
            lo, hi = st.slider("Plage", mn, mx, (mn, mx))
            apercu = prep.filter_numeric(df, col, lo, hi)
        elif mode == "Filtre categoriel" and cat:
            col = st.selectbox("Colonne", cat, key="f2")
            vals = st.multiselect("Valeurs", df[col].astype(str).unique().tolist())
            if vals:
                apercu = prep.filter_categorical(df, col, vals)
        elif mode == "Recherche textuelle":
            col = st.selectbox("Colonne", df.columns.tolist(), key="f3")
            q = st.text_input("Texte recherche")
            if q:
                apercu = prep.search_text(df, col, q)
        elif mode == "Tri":
            col = st.selectbox("Colonne", df.columns.tolist(), key="f4")
            asc = st.radio("Ordre", ["Ascendant", "Descendant"],
                           horizontal=True) == "Ascendant"
            apercu = prep.sort_values(df, col, asc)

        st.write(f"Resultat : **{apercu.shape[0]}** lignes")
        st.dataframe(apercu.head(100), width='stretch')
        if st.button("Appliquer ce filtre au dataset"):
            state.update_data(apercu.reset_index(drop=True), f"Filtrage ({mode})")
            _done()


def _done() -> None:
    """Notifie et rafraichit apres une operation de preprocessing."""
    notify_success("Operation appliquee avec succes.")
    st.rerun()
