# Mon Projet Django pour LITRevu

## 🚀 Introduction

Bienvenue dans **Mon Projet Django pour LITRevu** !  
Ce guide vous explique comment configurer et exécuter ce projet Django en local sur votre machine, de l’installation des dépendances à l’accès à l’application.

---

## ✅ Prérequis

Avant de commencer, assurez-vous d’avoir installé :

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/)
- Un éditeur de code (ex : VS Code)

---

## 📥 Installation et configuration locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/SebGris/project-9-django-web-LITRevu.git
cd project-9-django-web-LITRevu
```

### 2. Créer et activer un environnement virtuel

Sous Windows :
```bash
python -m venv env
env\Scripts\activate
```
Sous macOS/Linux :
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n’existe pas, créez-le avec :
```bash
pip freeze > requirements.txt
```

### 4. Installer Django et Pillow (si besoin)

```bash
pip install django
pip install Pillow
```
> **Remarque :** Pillow est indispensable pour la gestion des images avec Django (`ImageField`).

### 5. Appliquer les migrations

Créez la base de données et les tables nécessaires :
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur

Pour accéder à l’interface d’administration Django :
```bash
python manage.py createsuperuser
```
Suivez les instructions pour définir un nom d’utilisateur, une adresse email et un mot de passe.

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```
L’application sera alors disponible à l’adresse suivante :  
👉 http://127.0.0.1:8000/

### 8. (Optionnel) Démarrer le serveur Tailwind CSS

Si vous utilisez Tailwind CSS pour le style :
```bash
python manage.py tailwind start
```

### 9. Accès à l’administration Django

👉 http://127.0.0.1:8000/admin/  
Connectez-vous avec le superutilisateur créé précédemment.

### 10. (Optionnel) Exécuter les tests unitaires

```bash
python manage.py test
```

---

## 📄 Aide

Si vous rencontrez des problèmes, vérifiez que :
- l’environnement virtuel est bien activé
- toutes les dépendances sont installées (`pip install -r requirements.txt`)
- vous utilisez la bonne version de Python
- les migrations sont appliquées sans erreur

Sinon, consultez la documentation Django : https://docs.djangoproject.com/fr/

---

## ✨ À propos

Ce projet a été réalisé dans le cadre du parcours **Développeur d'application Python** – OpenClassrooms.
