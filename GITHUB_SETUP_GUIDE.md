# 📋 GUIDE COMPLET : METTRE TON PROJET SUR GITHUB

## 🎯 OBJECTIF

Créer un repository GitHub professionnel pour ton projet Monte Carlo qui impressionnera les recruteurs.

---

## 📦 ÉTAPE 1 : PRÉPARER LES FICHIERS (DÉJÀ FAIT ✅)

Tous les fichiers sont prêts dans le dossier `/asian-option-pricer/` :

```
asian-option-pricer/
├── README.md                    ✅ Documentation complète
├── LICENSE                      ✅ Licence MIT
├── requirements.txt             ✅ Dépendances Python
├── .gitignore                   ✅ Fichiers à ignorer
├── GETTING_STARTED.md          ✅ Guide de démarrage
├── setup_git.sh                ✅ Script de setup
│
├── src/
│   └── monte_carlo_pricer.py   ⚠️ À AJOUTER (ton code)
│
├── examples/
│   └── basic_usage.py          ✅ Exemples d'utilisation
│
├── visualizations/
│   └── (tes graphiques)        ⚠️ À AJOUTER (optionnel)
│
└── results/
    └── (tes résultats)         ⚠️ À AJOUTER (optionnel)
```

---

## 💻 ÉTAPE 2 : AJOUTER TON CODE

### Option A : Ligne de commande

```bash
# Copier ton fichier Python principal
cp /chemin/vers/ton/code.py asian-option-pricer/src/monte_carlo_pricer.py
```

### Option B : Manuellement

1. Ouvre ton fichier Python actuel (celui avec tout ton code Monte Carlo)
2. Copie tout le contenu
3. Crée le fichier `asian-option-pricer/src/monte_carlo_pricer.py`
4. Colle le code dedans

---

## 🌐 ÉTAPE 3 : CRÉER LE REPOSITORY SUR GITHUB

### 3.1 Aller sur GitHub

1. Va sur [github.com](https://github.com)
2. Connecte-toi (ou crée un compte si tu n'en as pas)

### 3.2 Créer un nouveau repository

1. Clique sur le **+** en haut à droite
2. Sélectionne **New repository**
3. Remplis les informations :

```
Repository name:    asian-option-pricer
Description:        Monte Carlo pricer for Asian options with variance reduction techniques achieving 73.8% variance improvement

Visibility:         ✅ Public (IMPORTANT pour que les recruteurs voient)

Initialize:         ❌ Ne coche RIEN (on a déjà les fichiers)
```

4. Clique **Create repository**

### 3.3 Noter l'URL

GitHub va te donner une URL comme :
```
https://github.com/TON_USERNAME/asian-option-pricer.git
```

**Note-la quelque part !**

---

## 🔧 ÉTAPE 4 : INSTALLER GIT (si pas déjà fait)

### Sur Windows

1. Télécharge depuis [git-scm.com/download/win](https://git-scm.com/download/win)
2. Installe avec les options par défaut
3. Ouvre **Git Bash**

### Sur Mac

```bash
# Dans Terminal
brew install git
```

### Sur Linux

```bash
sudo apt-get install git
```

### Vérifier l'installation

```bash
git --version
# Devrait afficher : git version 2.x.x
```

---

## 🚀 ÉTAPE 5 : CONFIGURER GIT (une seule fois)

```bash
# Ton nom (sera visible sur GitHub)
git config --global user.name "Thomas Nassar"

# Ton email (utilise celui de ton compte GitHub)
git config --global user.email "thomas.nassar@edu.ece.fr"

# Vérifier
git config --list
```

---

## 📤 ÉTAPE 6 : PUSHER TON CODE SUR GITHUB

### 6.1 Ouvrir le terminal dans le dossier du projet

```bash
cd /chemin/vers/asian-option-pricer
```

### 6.2 Initialiser Git

```bash
git init
```

Tu devrais voir : `Initialized empty Git repository...`

### 6.3 Ajouter tous les fichiers

```bash
git add .
```

### 6.4 Créer le premier commit

```bash
git commit -m "Initial commit: Asian option Monte Carlo pricer with variance reduction

- Implemented three variance reduction methods (basic MC, antithetic, control variates)
- Achieved 73.8% variance reduction with control variate method
- Integrated real market data via yfinance
- Asian-European correlation: ρ = 0.86
- Comprehensive documentation and examples included"
```

### 6.5 Connecter à GitHub

**Remplace TON_USERNAME par ton vrai username GitHub !**

```bash
git remote add origin https://github.com/TON_USERNAME/asian-option-pricer.git
```

### 6.6 Renommer la branche en "main"

```bash
git branch -M main
```

### 6.7 Pusher le code

```bash
git push -u origin main
```

### 6.8 Authentification

GitHub va te demander de t'authentifier :

**Option 1 : Personal Access Token (recommandé)**

1. Va sur GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Nom : "Git operations"
4. Durée : 90 days (ou plus)
5. Scopes : Coche **repo** (tout)
6. Generate token
7. **COPIE LE TOKEN** (tu ne le reverras plus !)
8. Quand Git demande le password, **colle le token** (pas ton mot de passe)

**Option 2 : GitHub CLI (plus simple)**

```bash
# Installer GitHub CLI
# Windows/Mac : https://cli.github.com

# Authentification
gh auth login

# Suivre les instructions
```

---

## ✅ ÉTAPE 7 : VÉRIFIER QUE ÇA A MARCHÉ

1. Va sur `https://github.com/TON_USERNAME/asian-option-pricer`
2. Tu devrais voir :
   - Ton README avec toute la documentation
   - Tous tes fichiers
   - Le badge vert "✅ Public"

**Si tu vois tout ça : BRAVO ! C'est en ligne ! 🎉**

---

## 📝 ÉTAPE 8 : AJOUTER LE LIEN DANS TON CV

### Dans l'en-tête du CV

```
Thomas NASSAR
thomas.nassar@edu.ece.fr - +33 6 52 73 26 90
LinkedIn: linkedin.com/in/thomas-nassar-a9935a290
GitHub: github.com/TON_USERNAME  ← AJOUTE ÇA
```

### Dans la section Projets

```
Monte Carlo pricer for Asian options with variance reduction

* Implemented Monte Carlo simulation... [Description]
* Technologies: Python (NumPy, Scipy)...

🔗 GitHub: github.com/TON_USERNAME/asian-option-pricer
```

---

## 🔄 COMMANDES UTILES POUR PLUS TARD

### Ajouter des modifications

```bash
# Après avoir modifié des fichiers
git add .
git commit -m "Add convergence analysis visualization"
git push
```

### Voir l'état

```bash
git status
```

### Voir l'historique

```bash
git log --oneline
```

### Annuler des modifications non commitées

```bash
git checkout -- fichier.py  # Annuler les modifs d'un fichier
git reset --hard            # Annuler TOUTES les modifs (⚠️ dangereux)
```

---

## 🎨 BONUS : RENDRE TON REPO ENCORE PLUS PRO

### 1. Ajouter des badges dans README.md

En haut du README, ajoute :

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

### 2. Ajouter des images

```bash
# Copier tes visualisations
cp mes_graphiques/*.png asian-option-pricer/visualizations/

# Commiter
git add visualizations/*.png
git commit -m "Add convergence and variance comparison plots"
git push
```

### 3. Créer un GitHub Pages (site web pour ton projet)

1. Va sur ton repo GitHub
2. Settings → Pages
3. Source : Deploy from branch → main → /root
4. Save

Ton projet aura maintenant un site web à :
`https://TON_USERNAME.github.io/asian-option-pricer`

---

## ❓ PROBLÈMES FRÉQUENTS

### "Permission denied"

**Solution :** Utilise un Personal Access Token au lieu de ton mot de passe

### "fatal: not a git repository"

**Solution :** Tu n'es pas dans le bon dossier. Fais `cd asian-option-pricer`

### "Updates were rejected"

**Solution :**
```bash
git pull origin main --rebase
git push
```

### "Authentication failed"

**Solution :** Ton token a expiré. Crée-en un nouveau sur GitHub

---

## 📞 BESOIN D'AIDE ?

1. Vérifie que tu as suivi TOUTES les étapes
2. Regarde les messages d'erreur (souvent ils expliquent le problème)
3. Google l'erreur exacte : "git error [ton message]"
4. Demande sur le Discord de l'école ou sur Stack Overflow

---

## 🎯 CHECKLIST FINALE

✅ Repository créé sur GitHub
✅ Code pushé et visible
✅ README.md s'affiche correctement
✅ Lien GitHub ajouté sur ton CV
✅ Repository est PUBLIC
✅ Pas de données sensibles (API keys, etc.)

---

**🎉 FÉLICITATIONS ! Ton projet est maintenant professionnel et visible par les recruteurs !**

Pour envoyer ce repo à un recruteur, envoie simplement :
```
github.com/TON_USERNAME/asian-option-pricer
```

Ils verront :
- Code propre et documenté
- README professionnel
- Résultats concrets (73.8% variance reduction)
- Exemples d'utilisation
- License

**C'est exactement ce qu'un recruteur veut voir ! 🚀**
