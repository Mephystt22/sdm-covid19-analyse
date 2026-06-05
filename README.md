# Sciences de Données Médicales — Analyse des données COVID-19

Application web interactive d'**analyse exploratoire**, de **nettoyage**, de
**prétraitement** et de **visualisation** de données cliniques COVID-19,
développée en **Python / Streamlit**.

> **Auteur :** Saad Elidrissi El Hassan
> **Formation :** 2ᵉ année Licence — Informatique Décisionnelle en Santé Digitale
> **Établissement :** UM6SS — École Supérieure Mohammed VI d'Ingénieurs en Sciences de la Santé
> **Sujet :** Analyse des données COVID-19 (*COVID-19 Clinical Dataset*)

---

## Fonctionnalités

- **Importation** de fichiers CSV avec aperçu, dimensions, types, statistiques,
  `df.info()`, détection automatique des colonnes numériques/catégorielles,
  détection des doublons et de la mémoire utilisée.
- **Analyse exploratoire** : statistiques complètes (moyenne, médiane, mode,
  variance, écart-type, min, max, quartiles), matrice de corrélation + heatmap,
  distributions (histogrammes, boxplots, densité, scatter, pie, bar), analyse
  des valeurs manquantes et des doublons.
- **Preprocessing** : gestion des valeurs manquantes (suppression / moyenne /
  médiane / mode / valeur personnalisée), suppression des doublons, détection
  et suppression des **outliers** (IQR / Z-score) avec visualisation
  avant/après, **normalisation**, **standardisation**, **encodage** (label /
  one-hot), renommage, changement de type, sélection de colonnes, filtrage
  dynamique, recherche et tri.
- **Visualisation** interactive (Plotly) et exportable (Matplotlib) :
  histogrammes, boxplots, heatmaps, corrélations, graphiques temporels, nuages
  de points, graphiques comparatifs — avec choix des colonnes, des couleurs et
  export.
- **Exportation** : dataset nettoyé (CSV / Excel), graphiques (PNG),
  statistiques descriptives, rapport d'analyse (Markdown).
- **Interface moderne** : sidebar de navigation, pages organisées, tableaux
  interactifs, KPI cards, **mode sombre**, design responsive.
- **Fonctionnalités avancées** : historique des traitements, sauvegarde
  automatique d'instantanés, aperçu avant/après, comparaison de datasets,
  tableau de bord analytique, barres de progression, notifications de
  succès/erreur, chargement dynamique.

---

## Architecture du projet

```
project/
├── app.py                 # Point d'entrée + navigation
├── pages/                 # Pages de l'application
│   ├── home.py            # Accueil / tableau de bord
│   ├── importation.py     # Importation des données
│   ├── exploration.py     # Analyse exploratoire
│   ├── preprocessing.py   # Nettoyage / transformation
│   ├── visualisation.py   # Visualisations interactives
│   ├── exportation.py     # Exportation des résultats
│   └── apropos.py         # À propos
├── utils/                 # Modules métier réutilisables
│   ├── data_loader.py     # Importation et inspection
│   ├── statistics.py      # Analyses statistiques
│   ├── preprocessing.py   # Fonctions de nettoyage
│   ├── visualization.py   # Génération des graphiques
│   ├── export.py          # Exportation (CSV/Excel/PNG/rapport)
│   ├── theme.py           # Thème, CSS, mode sombre, KPI cards
│   ├── state.py           # Gestion de l'état / historique
│   └── error_handler.py   # Gestion des erreurs + notifications
├── data/                  # Données
│   ├── covid19_clinical_dataset.csv
│   └── generate_dataset.py
├── exports/               # Dossier de sortie (généré)
├── assets/                # Ressources statiques
├── .streamlit/config.toml # Configuration et thème
├── requirements.txt
└── README.md
```

---

## Démarrage rapide

```bash
# 1. Créer et activer un environnement virtuel
python3 -m venv venv
source venv/bin/activate            # Linux / macOS
# .\venv\Scripts\activate           # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`.

>  Pour une installation détaillée sur **Fedora** et la **publication sur
> GitHub**, voir [`GUIDE_FEDORA_GITHUB.md`](GUIDE_FEDORA_GITHUB.md).

---

## Jeu de données

Le fichier `data/covid19_clinical_dataset.csv` contient des données cliniques
COVID-19 (âge, genre, mesures cliniques, comorbidités, sévérité, issue, etc.).
Il a été volontairement « bruité » (valeurs manquantes, doublons, valeurs
aberrantes) afin de démontrer toutes les fonctionnalités de nettoyage.
Vous pouvez le régénérer avec :

```bash
cd data && python3 generate_dataset.py
```

Vous pouvez également importer **votre propre fichier CSV** depuis la page
*Importation des données*.

---

## Stack technique

Python · Streamlit · Pandas · NumPy · Matplotlib · Plotly · OpenPyXL

---

© 2026 — Saad Elidrissi El Hassan. Projet académique.
