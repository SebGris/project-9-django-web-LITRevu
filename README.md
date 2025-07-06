# Projet Django pour LITRevu

Ce guide vous explique comment configurer et exécuter ce projet Django en local sur votre machine, de l’installation des dépendances à l’accès à l’application.

---

## ✅ Prérequis

Avant de commencer, assurez-vous d’avoir installé :

- [Python](https://www.python.org/downloads/) (version 3.8 ou supérieure)
- [pip](https://pip.pypa.io/en/stable/installation/) (généralement inclus avec Python)
- [Git](https://git-scm.com/downloads)
- [Node.js](https://nodejs.org/) (pour l'utilisation de Tailwind CSS)
- [Visual Studio Code](https://code.visualstudio.com/download)

---

## 📥 Configuration de l’environnement local

### 1. Cloner le dépôt

Ouvrir le terminal dans un dossier de travail (par exemple : `C:\Users\VotreNom\Documents\GitHub`) :
```bash
git clone https://github.com/SebGris/project-9-django-web-LITRevu.git
```
Ouvrez ensuite le dossier `project-9-django-web-LITRevu` dans Visual Studio Code.

### 2. Créer un environnement virtuel

Il est recommandé d’utiliser un environnement virtuel pour isoler les dépendances de votre projet.
Dans le terminal de Visual Studio Code, exécutez :
```bash
python -m venv venv
```

### 3. Activer l’environnement virtuel

Sur Windows :
```bash
venv\Scripts\activate
```
Sur macOS et Linux :
```bash
source venv/bin/activate
```

### 4. Installer les dépendances Python

Installez les dépendances nécessaires :
```bash
pip install -r requirements.txt
```

### 5. Installer les dépendances Node.js

Assurez-vous que Node.js est bien installé, puis exécutez :
```bash
npm install
```

### 6. Lancer le serveur de développement

⚠️ **Note** : Ce projet OpenClassrooms inclut une base de données SQLite avec des données de démonstration pour faciliter l'évaluation.

Démarrez le serveur Django :
```bash
python manage.py runserver
```

### 7. Accéder à l'application

Ouvrez votre navigateur aux adresses suivantes :

- **Application principale** : http://127.0.0.1:8000/
- **Interface d'administration** : http://127.0.0.1:8000/admin/  
- **Création de compte** : http://127.0.0.1:8000/signup/

---

## 📄 Aide

En cas de problème, vérifiez que :

- l'environnement virtuel est bien activé (`venv\Scripts\activate` sur Windows)
- toutes les dépendances sont installées (`pip install -r requirements.txt`)
- vous utilisez une version compatible de Python (3.8+)
- Node.js est installé pour Tailwind CSS

Consultez aussi la documentation officielle :  
👉 https://docs.djangoproject.com/fr/
👉 https://docs.djangoproject.com/fr/5.2/topics/db/queries/
👉 https://docs.djangoproject.com/fr/5.2/ref/models/querysets/#queryset-api
👉 https://docs.djangoproject.com/fr/5.2/topics/db/queries/#complex-lookups-with-q-objects
👉 https://docs.djangoproject.com/fr/5.2/topics/db/aggregation/#generating-aggregates-for-each-item-in-a-queryset
👉 https://realpython.com/python-pyproject-toml/

### Commandes utiles

```bash
# Créer un superutilisateur (si nécessaire)
python manage.py createsuperuser

# Démarrer Tailwind en mode développement (optionnel)
python manage.py tailwind start

# Lancer les tests
python manage.py test
```

### Fonctionnalités principales

- **Authentification** : Inscription, connexion, déconnexion
- **Tickets** : Demander des critiques de livres/articles
- **Critiques** : Publier des critiques avec notes (1-5 étoiles)
- **Abonnements** : Suivre d'autres utilisateurs
- **Flux** : Voir l'activité des utilisateurs suivis

---

## ✨ À propos

Ce projet a été réalisé dans le cadre du parcours **Développeur d'application Python** – OpenClassrooms.
