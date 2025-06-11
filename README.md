# 🥗 Projet Alimentation – Version Flask

## 📚 Description

Ce projet est une application web back-end développée avec **Flask** qui permet à des utilisateurs de simuler leur alimentation, signaler des allergies, gérer un buffet pour des cérémonies, et planifier leurs repas hebdomadaires. Le projet est conteneurisé avec **Docker** et s'appuie sur une base de données **PostgreSQL**. Les plats proposés sont des oeuvres d'art représentant l'art culinaire sénégalais entre autres : La thiéboudienne, les beignets pastels, le poulet Yassa, La sauce Mafé, et le ragoût Domoda.

## 📦 Fonctionnalités principales

| Fonctionnalité                          | Description |
|-----------------------------------------|-------------|
| 🧑‍💼 Authentification utilisateur         | Inscription connexion, gestion de session.                                           |
| 🍛 Gestion des plats                    | Chaque plat a 20 images et une liste d’ingrédients.                                  |
| 🤧 Détection d’allergie                 | Un utilisateur est déclaré allergique si le ratio allergie/consommation dépasse 30%. |
| 📷 Affichage aléatoire d’images         | Une image aléatoire parmi les 20 disponibles pour un plat est affichée.              |
| 🍽️ Gestion de buffet                    | Création et modification de buffets pour les cérémonies.                             |
| 📅 Planification hebdomadaire           | L’utilisateur planifie ses repas pour la semaine.                                    |
| ⚙️ API REST                             | Chaque service est exposé via une API (POST, GET, PUT, DELETE).                      |
| 🐳 Conteneurisation Docker              | Exécution sur n’importe quelle plateforme via Docker.                                |

## 🧱 Architecture du projet

Projet_alimentation/
├── app/
│ ├── __init__.py
│ ├── config.py
│ ├── models/
│ │ ├── __init__.py
│ │ ├── allergie_declaree.py
│ │ ├── buffet.py
│ │ ├── consommation.py
│ │ ├── image_plat.py
│ │ ├── planning.py
│ │ ├── plats.py
│ │ └── utilisateur.py
│ ├── routes/
│ │ ├── __init__.py
│ │ ├── auth.py
│ │ ├── buffet.py
│ │ ├── consommation.py
│ │ ├── planning.py
│ │ └── plats.py
│ ├── templates/
│ └── static/
├── data/
│ ├── users.json
│ ├── plats.json
│ └── ...
├── import_json.py
├── run.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md

## 🚀 Lancer le projet en local

### 1. 📥 Cloner le dépôt

git clone https://github.com/DavidTchami3003/projet_alimentation.git

cd projet_alimentation

### 2. 🐳 Lancer avec Docker

sudo docker compose up --build

### 3. 💾 Importer les données initiales

Après avoir démarré l'application avec Docker :

docker-compose up --build -d

Initialise les tables de la BD ( Opération à ne faire qu'une fois):

docker exec -it flask_app python init_bd.py

Lance le script d'importation des données depuis le conteneur :

docker exec -it flask_app python import_json.py

Cela insérera les utilisateurs, plats dans la base PostgreSQL.

Attention : Les deux dernières opérations sont  effectuer sur un autre terminal ouvert sur le dossier racine du projet

### 3. 🌐 Accéder à l’application

Ouvre Postman et l'adresse à utiliser pour exécuter les requêtes API est :
http://localhost:5000

🔁 Flux de fonctionnement

🔐 Authentification

Inscription avec nom d'utilisateur et mot de passe.

Connexion et gestion de session.

Déconnexion à tout moment.

Seul l'administrateur a le droit de voir tous les comptes présent dans la BD et de les supprimer

🍽️ Simulation de consommation

Choix du plat.

Affichage d’une image aléatoire.

Signalement d’une allergie éventuelle.

Suivi du ratio allergie/consommation.

Le système mémorise les consommations

Déclaration d’allergie à un plat si le ratio allergie > 30% après au moins 4 consommations de ce plat.

🎉 Buffet de cérémonie

Création de buffets personnalisés.

Ajout ou retrait de plats.

Suppression d'un buffet ou de tous les buffets

Association à un utilisateur.

📅 Planification hebdomadaire

Le système génère un planning de plat à consommer pour les 7 jours de la semaine.

Possibilité de changer le plat d'un jour

Possibilité de supprimer un le planning journalier ainsi que tout le planning

Vue hebdomadaire par utilisateur.

Les données sont enregistrées dans la base PostgreSQL

## 📡 Endpoints principaux (API)

Méthode	    URL	                              Description                                   Exemle modèle JSON
Utilsateur 
POST	    /api/register	                  Inscription utilisateur                       {"username":"nom","password":"mdp"}
POST	    /api/login	                      Connexion                                     idem
PUT         /api/users                        Update ses infos                              idem ou un des deux champs
POST	    /api/logout	                      Déconnexion   
GET         /api/users                        Liste des utilisateurs (Admin only)
GET         /api/users/<id>                   Obtenir les infos d'un user (Admin only)
DELETE      /api/users/<id>                   Supprimer un utilisateur (Admin only)

Plats
GET	        /api/plats	                      Obtenir la liste des plats
POST        /api/plats                        Créer un plat                                 {"nom":"nom","ingredients":"ingr","image_path":"path"} Uniquement le nom est requis
GET         /api/plats/<plat_id>              Obtenir les infos d'un plat
PUT         /api/plats/<plat_id>              Update les information d'un plat
GET         /api/plats/<plat_id>/image        Obtenir une image aléatoire d'un plat
DELETE      /api/plats/<plat_id>              Supprimer un plat
GET         /api/plats/plats_allergiques      Obtenir la liste des plats allergènes

Consommation
GET         /api/consommations                Obtenir toutes les consommations        
GET         /api/consommations/<plat_id>      Obtenir une consommation
DELETE      /api/consommations                Supprimer toutes les consommations
DELETE      /api/consommations/<plat_id>      Supprimer une consommation
POST        /api/manger                       Manger un plat                                {"plat_id":1,"allergique":False}
GET         /api/statut/<plat_id>             Verifier si allergique à un plat

Buffet
POST        /api/buffets/generer              Générer un buffet                             {"nom":"buff1",date:"YYYY-MM-DD","lieu":"UY1","plats":[3,5]}
GET         /api/buffets                      Obtenir la liste des buffets
GET         /api/buffets/<buffet_id>          Obtenir les infos d'un buffet
DELETE      /api/buffets                      Supprimer tous les buffets
DELETE      /api/buffets/<buffet_id>          Supprimer un buffet
PUT         /api/buffets/<id>/ajouter_plats   Ajouter un/des plats à un buffet              {"plats":[1,2,4,5]}
PUT         /api/buffets/<id>/retirer_plats   Retirer un/des plat d'un buffet               {"plats":[2]}

Planning
POST        /api/planning/generer             Générer un planning                           
GET         /api/planning                     Voir le planning
PUT         /api/planning/<str:jour>          Modifier le plat d'un jour                    {"plat_id":4}
DELETE      /api/planning/<jour_id>           Supprimer un planning journalier
DELETE      /api/planning                     Supprimer tout le planning

## 🗃️ Technologies utilisées

Python 3
Flask
SQLAlchemy
PostgreSQL
Docker
Git
Postman (test d’API)

## 🤝 Auteurs

Tchami Fetmonou David Stive alias Dr Scam 