# Rapport détaillé du projet
## Sciences de Données Médicales — Analyse des données COVID-19

**Auteur :** Saad Elidrissi El Hassan
**Formation :** 2ᵉ année Licence — Informatique Décisionnelle en Santé Digitale
**Établissement :** UM6SS — École Supérieure Mohammed VI d'Ingénieurs en Sciences de la Santé
**Sujet :** Analyse des données COVID-19 (*COVID-19 Clinical Dataset*)

---

## 1. Introduction

Ce projet consiste à développer une application web interactive, en
**Python / Streamlit**, dédiée à l'analyse exploratoire, au nettoyage, au
prétraitement et à la visualisation de données cliniques COVID-19.
L'objectif est de fournir une plateforme complète permettant à un utilisateur
non-développeur d'importer un jeu de données, de le comprendre, de le nettoyer
et d'en exporter les résultats — sans écrire une seule ligne de code.

Le jeu de données utilisé décrit des patients atteints de la COVID-19 :
données démographiques (âge, genre, pays), mesures cliniques (température,
saturation en oxygène, fréquence cardiaque, CRP, D-dimères, valeur Ct de PCR…),
comorbidités (diabète, hypertension, maladie cardiaque), statut vaccinal,
sévérité des symptômes et issue (guéri / décédé).

---

## 2. Architecture du projet

L'application suit une architecture **modulaire** séparant clairement
l'interface (pages) de la logique métier (utils).

```
project/
├── app.py             point d'entrée, navigation, thème
├── pages/             une page = une fonction render()
│   ├── home.py, importation.py, exploration.py,
│   ├── preprocessing.py, visualisation.py,
│   └── exportation.py, apropos.py
├── utils/             modules métier réutilisables
│   ├── data_loader.py    (importation, inspection)
│   ├── statistics.py     (analyses statistiques)
│   ├── preprocessing.py  (nettoyage, transformations)
│   ├── visualization.py  (graphiques Plotly / Matplotlib)
│   ├── export.py         (CSV, Excel, PNG, rapport)
│   ├── theme.py          (CSS, mode sombre, KPI cards)
│   ├── state.py          (état, historique, instantanés)
│   └── error_handler.py  (gestion d'erreurs, notifications)
├── data/              dataset + générateur
├── exports/, assets/, .streamlit/config.toml
└── requirements.txt, README.md
```

**Choix de conception :**
- chaque module `utils/*` est **indépendant et testable** ;
- l'**état applicatif** (dataset courant, original, historique) est centralisé
  dans `st.session_state` via `utils/state.py`, garantissant la persistance
  entre les pages ;
- la **gestion des erreurs** est centralisée par le décorateur `@safe` qui
  capture toute exception et l'affiche proprement ;
- le **thème** (clair / sombre) est injecté dynamiquement en CSS.

> _**[Capture d'écran 1 à insérer ici]** : page d'accueil avec le tableau de
> bord et les KPI cards._

---

## 3. Importation et inspection des données

Le module `data_loader.py` lit le CSV de manière robuste (détection
automatique du séparateur et des colonnes de dates). Après importation,
l'application affiche :
l'aperçu du dataset, ses dimensions, les types de colonnes, les statistiques
descriptives, la sortie de `df.info()`, la **détection automatique** des
colonnes numériques / catégorielles / temporelles, le **nombre de doublons** et
la **mémoire utilisée**.

> _**[Capture d'écran 2 à insérer ici]** : page Importation après chargement du
> dataset COVID-19._

---

## 4. Analyse statistique

Le module `statistics.py` calcule, pour chaque variable numérique : moyenne,
médiane, mode, variance, écart-type, minimum, maximum et quartiles (Q1, Q3).
Il fournit également la **matrice de corrélation** (Pearson / Spearman),
la **table des valeurs manquantes** (effectif et pourcentage) et l'extraction
des **lignes dupliquées**.

**Quelques résultats sur le jeu de données (après suppression des doublons,
1 400 patients) :**

| Indicateur | Valeur |
|------------|--------|
| Âge moyen | ≈ 53,5 ans |
| Mortalité globale | ≈ 2,7 % |
| Répartition de la sévérité | Mild 53 % · Moderate 40 % · Severe 7 % · Critical < 1 % |
| Mortalité chez les cas « Severe » | ≈ 24 % |

La mortalité croît fortement avec la sévérité des symptômes, ce qui est
cohérent sur le plan clinique. L'admission en soins intensifs est très
corrélée au recours au **ventilateur** (≈ 0,84), puis, plus faiblement, à
l'hospitalisation, au diabète et à l'âge.

> _**[Capture d'écran 3 à insérer ici]** : onglet Statistiques et heatmap de
> corrélation._

---

## 5. Preprocessing (nettoyage et transformation)

Le jeu de données fourni a été **volontairement bruité** afin d'illustrer
toutes les fonctionnalités : 570 valeurs manquantes réparties sur plusieurs
colonnes, 25 doublons, et des valeurs aberrantes évidentes (âge à 255 ans,
température à 50 °C, fréquence cardiaque à 400 bpm).

Le module `preprocessing.py` permet :

1. **Valeurs manquantes** — suppression de lignes/colonnes, imputation par
   moyenne, médiane, mode ou valeur personnalisée.
2. **Doublons** — suppression automatique.
3. **Outliers** — détection par **IQR** ou **Z-score**, suppression et
   **visualisation avant/après** (boxplots).
4. **Transformations** — normalisation Min-Max, standardisation Z-score,
   encodage **label** ou **one-hot**, renommage de colonnes, changement de type.
5. **Sélection de colonnes** — suppression ou conservation des variables utiles.
6. **Filtrage** — filtres dynamiques (numériques et catégoriels), recherche
   textuelle et tri.

Chaque opération met à jour le dataset courant, **journalise l'action** dans
l'historique et conserve un **instantané** pour la comparaison avant/après.

> _**[Capture d'écran 4 à insérer ici]** : onglet Outliers avant/après._

---

## 6. Visualisation des données

Le module `visualization.py` génère des graphiques **interactifs** (Plotly) et
**exportables** (Matplotlib) : histogrammes, boxplots, courbes de densité,
nuages de points, diagrammes circulaires et en barres, heatmaps de corrélation,
graphiques temporels (évolution hebdomadaire des admissions) et graphiques
comparatifs (statistique d'une variable numérique par catégorie).
L'utilisateur choisit les colonnes, les couleurs et le nombre de classes, puis
peut exporter le graphique.

> _**[Capture d'écran 5 à insérer ici]** : page Visualisations avec un graphique
> temporel ou comparatif._

---

## 7. Exportation des résultats

Le module `export.py` permet de télécharger : le dataset nettoyé en **CSV** et
en **Excel** (via OpenPyXL), les graphiques en **PNG**, les statistiques
descriptives, et un **rapport d'analyse** complet au format Markdown généré
automatiquement (résumé du dataset, statistiques, valeurs manquantes,
historique des traitements). La page propose également une **comparaison
avant/après** (lignes et valeurs manquantes du dataset original vs nettoyé).

> _**[Capture d'écran 6 à insérer ici]** : page Exportation et comparaison
> avant/après._

---

## 8. Fonctionnalités avancées

- **Mode sombre** activable depuis la barre latérale (thème CSS dynamique).
- **Historique des traitements** horodaté, consultable à tout moment.
- **Sauvegarde automatique** d'instantanés et **réinitialisation** au dataset
  original.
- **Aperçu et comparaison avant/après** nettoyage.
- **Tableau de bord analytique** sur la page d'accueil (KPI cards + aperçus).
- **Barres de progression** lors du chargement.
- **Notifications** de succès / erreur (toasts).
- **Chargement dynamique** des données et **gestion robuste des erreurs**.

---

## 9. Conclusion

L'application répond à l'ensemble du cahier des charges : importation,
analyse exploratoire, preprocessing complet, visualisation interactive et
exportation, le tout dans une interface moderne, claire et professionnelle.
L'architecture modulaire facilite la maintenance et l'extension du projet
(ajout de nouveaux graphiques, de nouvelles transformations ou de nouveaux
formats d'export).

---

© 2026 — Saad Elidrissi El Hassan. Projet académique.
