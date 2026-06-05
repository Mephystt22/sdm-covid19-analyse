# Guide d'installation sur Fedora & publication sur GitHub

Ce guide vous accompagne **pas à pas** pour :

1. installer et exécuter le projet sur **Fedora**,
2. le **publier sur votre compte GitHub** (`Saad Elidrissi El Hassan`).

Toutes les commandes sont à exécuter dans un **terminal** (application
*Terminal* sur Fedora).

---

## Partie 1 — Installer et lancer l'application sur Fedora

### 1.1 Vérifier / installer Python

Fedora est livré avec Python 3. Vérifiez la version (3.9+ requis) :

```bash
python3 --version
```

Si Python n'est pas installé ou trop ancien :

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv
```

### 1.2 Récupérer le projet

Décompressez l'archive ZIP du projet, puis placez-vous dans le dossier :

```bash
cd ~/Téléchargements
unzip projet_sdm_covid19.zip      # adaptez le nom de l'archive
cd project
```

> Vous pouvez aussi déplacer le dossier ailleurs, par exemple
> `mv project ~/projet_sdm && cd ~/projet_sdm`.

### 1.3 Créer un environnement virtuel

L'environnement virtuel isole les dépendances du projet du reste du système.

```bash
python3 -m venv venv
source venv/bin/activate
```

Le prompt affiche désormais `(venv)` au début de la ligne. Pour quitter
l'environnement plus tard : `deactivate`.

### 1.4 Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

>  Le paquet `kaleido` (export PNG des graphiques Plotly) est optionnel.
> S'il pose problème, l'application bascule automatiquement sur un export HTML.

### 1.5 Lancer l'application

```bash
streamlit run app.py
```

Streamlit ouvre automatiquement votre navigateur sur
`http://localhost:8501`. Sinon, ouvrez ce lien manuellement.

Pour **arrêter** l'application : `Ctrl + C` dans le terminal.

### 1.6 (Optionnel) Régénérer le jeu de données

```bash
cd data
python3 generate_dataset.py
cd ..
```

### Dépannage rapide

| Problème | Solution |
|----------|----------|
| `command not found: streamlit` | L'environnement virtuel n'est pas activé : `source venv/bin/activate` |
| Le port 8501 est occupé | Lancez sur un autre port : `streamlit run app.py --server.port 8502` |
| Pare-feu bloque l'accès réseau | `sudo firewall-cmd --add-port=8501/tcp` (session courante) |
| Erreur de compilation d'un paquet | `sudo dnf install -y gcc python3-devel` puis relancez `pip install` |

---

## Partie 2 — Publier le projet sur GitHub

### 2.1 Installer et configurer Git

```bash
sudo dnf install -y git
git config --global user.name "Saad Elidrissi El Hassan"
git config --global user.email "votre.email@exemple.com"
```

> Utilisez l'adresse e-mail associée à votre compte GitHub.

### 2.2 Créer un dépôt vide sur GitHub

1. Connectez-vous sur <https://github.com>.
2. Cliquez sur **New repository** (bouton vert *New*).
3. **Repository name** : par exemple `sdm-covid19-analyse`.
4. Laissez le dépôt **vide** : *ne cochez pas* « Add a README »,
   `.gitignore` ou licence (ils existent déjà dans le projet).
5. Cliquez sur **Create repository**.

GitHub affiche alors l'URL du dépôt, par exemple :
`https://github.com/<votre-utilisateur>/sdm-covid19-analyse.git`.

### 2.3 Initialiser le dépôt local

Depuis le dossier `project/` :

```bash
git init
git add .
git commit -m "Initial commit : application SDM COVID-19"
git branch -M main
```

> Le fichier `.gitignore` fourni empêche d'envoyer l'environnement virtuel
> (`venv/`), les caches Python et les fichiers d'export.

### 2.4 Relier le dépôt local à GitHub et pousser

```bash
git remote add origin https://github.com/<votre-utilisateur>/sdm-covid19-analyse.git
git push -u origin main
```

### 2.5 S'authentifier

GitHub n'accepte **plus le mot de passe** pour le push. Deux options :

**Option A — Token d'accès personnel (le plus simple)**

1. Sur GitHub : *Settings  Developer settings  Personal access tokens 
   Tokens (classic)  Generate new token*.
2. Cochez la portée **`repo`**, générez le token et **copiez-le**.
3. Lors du `git push`, saisissez votre **nom d'utilisateur** puis collez le
   **token** à la place du mot de passe.

**Option B — Clé SSH (pratique pour la suite)**

```bash
ssh-keygen -t ed25519 -C "votre.email@exemple.com"   # appuyez sur Entrée à chaque question
cat ~/.ssh/id_ed25519.pub                              # copiez la clé affichée
```

Puis sur GitHub : *Settings  SSH and GPG keys  New SSH key*, collez la clé.
Changez ensuite l'URL distante pour utiliser SSH :

```bash
git remote set-url origin git@github.com:<votre-utilisateur>/sdm-covid19-analyse.git
git push -u origin main
```

### 2.6 Mettre à jour le dépôt plus tard

À chaque modification du projet :

```bash
git add .
git commit -m "Description de la modification"
git push
```

---

## Récapitulatif des commandes essentielles

```bash
# Installation et lancement
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

# Publication GitHub
git init && git add . && git commit -m "Initial commit"
git branch -M main
git remote add origin <URL-du-dépôt>
git push -u origin main
```

---

© 2026 — Saad Elidrissi El Hassan.
