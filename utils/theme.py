"""
utils/theme.py
--------------
Theme visuel de l'application : design medical moderne, minimaliste et epure.

Principes de conception :
    - palette calme et apaisante (bleus doux, teal/sarcelle, gris clairs, blancs),
    - typographie sans-serif moderne (Inter / Segoe UI),
    - conteneurs ("cards") a coins arrondis et ombres douces,
    - espacement genereux pour une lecture confortable,
    - masquage des menus par defaut de Streamlit (aspect application native),
    - aucun emoji ni symbole graphique (esthetique purement professionnelle).

Fournit egalement un mode sombre entierement lisible (chrome, texte, cartes,
onglets, champs, tableaux et graphiques).

Auteur : Saad Elidrissi El Hassan
"""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------
# Palettes (clair / sombre)
# ---------------------------------------------------------------------
LIGHT = {
    "bg": "#F5F8FA",          # fond general (blanc bleute)
    "card": "#FFFFFF",        # fond des cartes
    "elevated": "#FFFFFF",
    "text": "#1F2D3D",        # texte principal
    "muted": "#6B7C8E",       # texte secondaire
    "primary": "#0E7C7B",     # teal / sarcelle
    "primary_soft": "#14B8A6",
    "blue": "#3E7CB1",        # bleu doux
    "border": "#E5EBF0",
    "shadow": "0 1px 3px rgba(16,42,67,.06), 0 10px 28px rgba(16,42,67,.05)",
    "input_bg": "#FFFFFF",
}
DARK = {
    "bg": "#0F1A24",
    "card": "#17242F",
    "elevated": "#1C2C39",
    "text": "#E6EEF5",
    "muted": "#9DB0BF",
    "primary": "#2BB7B3",
    "primary_soft": "#43C9C4",
    "blue": "#6FA8DC",
    "border": "#26384A",
    "shadow": "0 1px 3px rgba(0,0,0,.35), 0 10px 28px rgba(0,0,0,.30)",
    "input_bg": "#1C2C39",
}

# Palette calme reutilisee par les graphiques (teal + bleus doux)
CHART_SEQUENCE = ["#0E7C7B", "#3E7CB1", "#14B8A6", "#6FA8DC",
                  "#8FD4D2", "#A9C9E8", "#0D9488", "#5B8DC9"]


def palette() -> dict:
    """Retourne la palette active selon le mode (sombre ou clair)."""
    return DARK if st.session_state.get("dark_mode") else LIGHT


def charger_style_css() -> None:
    """Injecte le CSS global de l'application (theme + composants).

    C'est la fonction centrale du design : elle construit la feuille de style
    a partir de la palette active et l'injecte via st.markdown.
    """
    c = palette()
    dark = st.session_state.get("dark_mode", False)

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {{
            --bg: {c['bg']};
            --card: {c['card']};
            --elevated: {c['elevated']};
            --text: {c['text']};
            --muted: {c['muted']};
            --primary: {c['primary']};
            --primary-soft: {c['primary_soft']};
            --blue: {c['blue']};
            --border: {c['border']};
            --shadow: {c['shadow']};
            --input-bg: {c['input_bg']};
            --radius: 16px;
        }}

        /* ---- Typographie globale ---- */
        html, body, [class*="css"], .stApp {{
            font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
        }}

        /* ---- Fond et couleur de texte de base ---- */
        .stApp {{ background: var(--bg); color: var(--text); }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        .stApp p, .stApp span, .stApp label, .stApp li, .stApp div,
        [data-testid="stMarkdownContainer"] {{ color: var(--text); }}
        .stApp a {{ color: var(--blue); }}

        /* ---- Masquage des menus Streamlit (aspect application native) ---- */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        [data-testid="stToolbar"] {{ display: none; }}
        [data-testid="stDecoration"] {{ display: none; }}
        header[data-testid="stHeader"] {{ background: transparent; height: 0; }}
        .block-container {{ padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1200px; }}

        /* ---- Barre laterale ---- */
        section[data-testid="stSidebar"] {{
            background: var(--card);
            border-right: 1px solid var(--border);
        }}
        section[data-testid="stSidebar"] * {{ color: var(--text); }}

        /* ---- Titres de l'application ---- */
        .app-title {{
            font-size: 1.8rem; font-weight: 800; letter-spacing: -.01em;
            color: var(--text); margin-bottom: .25rem; line-height: 1.2;
        }}
        .app-subtitle {{ color: var(--muted); font-size: .98rem; margin-top: 0; }}
        .section-title {{
            font-size: 1.18rem; font-weight: 700; color: var(--text);
            margin: 1.6rem 0 .9rem 0; padding-left: .75rem;
            border-left: 3px solid var(--primary);
        }}
        .brand {{ font-size: 1.15rem; font-weight: 800; color: var(--primary);
                  letter-spacing: -.01em; }}
        .brand-sub {{ color: var(--muted); font-size: .8rem; }}

        /* ---- Cartes KPI ---- */
        .kpi-card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.1rem 1.25rem;
            box-shadow: var(--shadow);
            position: relative; overflow: hidden;
            transition: transform .18s ease, box-shadow .18s ease;
        }}
        .kpi-card::before {{
            content: ""; position: absolute; left: 0; top: 0; bottom: 0;
            width: 4px; background: linear-gradient(180deg, var(--primary), var(--blue));
        }}
        .kpi-card:hover {{ transform: translateY(-2px);
                           box-shadow: 0 14px 32px rgba(16,42,67,.12); }}
        .kpi-label {{ color: var(--muted); font-size: .76rem; font-weight: 600;
                      text-transform: uppercase; letter-spacing: .06em; }}
        .kpi-value {{ color: var(--text); font-size: 1.7rem; font-weight: 800;
                      margin-top: .25rem; line-height: 1.1; }}

        /* ---- Carte generique ---- */
        .med-card {{
            background: var(--card); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 1.25rem 1.4rem;
            box-shadow: var(--shadow);
        }}

        /* ---- Boutons ---- */
        .stButton > button, .stDownloadButton > button {{
            border-radius: 10px; font-weight: 600; border: 1px solid var(--border);
            background: var(--card); color: var(--text);
            transition: all .15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: var(--primary); color: var(--primary);
        }}
        .stButton > button[kind="primary"] {{
            background: var(--primary); color: #FFFFFF; border-color: var(--primary);
        }}

        /* ---- Onglets ---- */
        .stTabs [data-baseweb="tab-list"] {{ gap: .25rem; border-bottom: 1px solid var(--border); }}
        .stTabs [data-baseweb="tab"] {{ color: var(--muted); font-weight: 600; }}
        .stTabs [aria-selected="true"] {{ color: var(--primary); }}
        .stTabs [data-baseweb="tab-highlight"] {{ background: var(--primary); }}

        /* ---- Champs de saisie / selecteurs (lisibilite en mode sombre) ---- */
        [data-baseweb="input"], [data-baseweb="select"] > div,
        [data-baseweb="textarea"] {{
            background: var(--input-bg) !important; color: var(--text) !important;
            border-radius: 10px !important;
        }}
        [data-baseweb="select"] span, [data-baseweb="input"] input {{ color: var(--text) !important; }}
        .stSlider label, .stRadio label, .stCheckbox label {{ color: var(--text); }}

        /* ---- Metriques natives, expander, alertes ---- */
        [data-testid="stMetricValue"] {{ color: var(--text); }}
        [data-testid="stMetricLabel"] {{ color: var(--muted); }}
        details, [data-testid="stExpander"] {{
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px;
        }}
        [data-testid="stExpander"] summary {{ color: var(--text); }}

        /* ---- Tableaux : conteneur et coins arrondis ---- */
        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            border-radius: 12px; overflow: hidden; border: 1px solid var(--border);
        }}
        {".stDataFrame, [data-testid='stDataFrame'] * { color: var(--text); }" if dark else ""}

        /* ---- Code blocks ---- */
        .stCode, pre, code {{ border-radius: 10px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Alias retro-compatible (ancien nom utilise dans le code)
def inject_css() -> None:
    """Alias de charger_style_css() (compatibilite)."""
    charger_style_css()


# ---------------------------------------------------------------------
# Composants reutilisables
# ---------------------------------------------------------------------
def page_header(title: str, subtitle: str = "") -> None:
    """Affiche un en-tete de page standardise (titre + sous-titre)."""
    st.markdown(f'<div class="app-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="app-subtitle">{subtitle}</p>',
                    unsafe_allow_html=True)


def section_title(text: str) -> None:
    """Affiche un titre de section stylise."""
    st.markdown(f'<div class="section-title">{text}</div>',
                unsafe_allow_html=True)


def kpi_card(label: str, value, accent: str | None = None) -> None:
    """Affiche une carte KPI epuree (a placer dans une colonne).

    Aucune icone ni emoji : seule la typographie et l'accent colore
    structurent la carte, conformement a la charte graphique.
    """
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plotly_template() -> str:
    """Template Plotly adapte au mode courant."""
    return "plotly_dark" if st.session_state.get("dark_mode") else "plotly_white"


def style_fig(fig):
    """Applique la charte graphique a une figure Plotly (couleurs, fond, marges).

    Garantit que les graphiques s'integrent a l'esthetique de l'application
    et restent lisibles en mode clair comme en mode sombre.
    """
    c = palette()
    fig.update_layout(
        template=plotly_template(),
        font=dict(family="Inter, Segoe UI, sans-serif", color=c["text"], size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=CHART_SEQUENCE,
        margin=dict(l=10, r=10, t=50, b=10),
        title_font=dict(size=16, color=c["text"]),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=c["border"], zerolinecolor=c["border"])
    fig.update_yaxes(gridcolor=c["border"], zerolinecolor=c["border"])
    return fig
