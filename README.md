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

Démarrez le serveur Django :
```bash
python manage.py runserver
```
Puis ouvrez votre navigateur à l’adresse : http://127.0.0.1:8000/

Accès à l’administration Django :  http://127.0.0.1:8000/admin/  
Connectez-vous avec le superutilisateur créé auparavant.

---

## 📄 Aide

En cas de problème, vérifiez que :

- l’environnement virtuel est bien activé
- toutes les dépendances sont installées (`pip install -r requirements.txt`)
- vous utilisez une version compatible de Python
- les migrations ont été correctement appliquées

Consultez aussi la documentation officielle :  
👉 https://docs.djangoproject.com/fr/
👉 https://docs.djangoproject.com/fr/5.2/topics/db/queries/
👉 https://docs.djangoproject.com/fr/5.2/ref/models/querysets/#queryset-api
👉 https://docs.djangoproject.com/fr/5.2/topics/db/queries/#complex-lookups-with-q-objects
👉 https://docs.djangoproject.com/fr/5.2/topics/db/aggregation/#generating-aggregates-for-each-item-in-a-queryset

---

## ✨ À propos

Ce projet a été réalisé dans le cadre du parcours **Développeur d'application Python** – OpenClassrooms.