# ETL Data Pipeline Project with Docker


## Objectif du Projet
Ce projet implémente un pipeline ETL (Extraction, Transformation, Chargement) en utilisant Docker, Python, PostgreSQL et Metabase. Il est conçu pour extraire des données à partir de fichiers CSV, les transformer selon des règles spécifiques, et les charger dans une base de données PostgreSQL. Les données transformées sont ensuite accessibles pour exploration et visualisation via Metabase.

## Fonctionnalités principales
* **Extraction** : Importation de données depuis des fichiers CSV.
* **Transformation** : Nettoyage des données, gestion des valeurs manquantes, ajout de colonnes calculées, filtrage des données indésirables, etc.
* **Chargement** : Insertion des données transformées dans une base de données PostgreSQL pour un accès centralisé.
* **Exploration et Visualisation** : Utilisation de Metabase pour interroger et visualiser les données.


## Pré-requis
Pour exécuter ce projet, vous aurez besoin de :

* **Docker et Docker Compose**
* **git pour cloner le dépôt**
Optionnel : Python (si vous souhaitez exécuter le script ETL en dehors de Docker pour des tests locaux)

## Architecture
L’architecture de ce projet se compose des éléments suivants :

1. Docker pour orchestrer les différents conteneurs.
2. PostgreSQL pour stocker les données en tant que data warehouse.
3. Python pour le script ETL qui extrait, transforme et charge les données.
4. Metabase pour la visualisation des données.
Les composants sont configurés pour fonctionner ensemble dans un environnement conteneurisé, simplifiant le déploiement et l’évolutivité.

## Installation
1. **Cloner le dépôt**

`git clone https://github.com/ton_utilisateur/ETL_DataPipeline_Docker.git`
`cd ETL_DataPipeline_Docker`

2. **Configurer les Variables d’Environnement**
Créez un fichier .env à la racine du projet avec les informations suivantes :


    DWH_USER=your_username
    DWH_PASSWORD=your_password
    DWH_DB=your_database_name
    DWH_HOST=warehouse
    DWH_PORT=5432
Ces variables seront utilisées par le conteneur PostgreSQL et le script ETL pour se connecter à la base de données.

3. **Exécuter le Projet avec Docker Compose**
Pour lancer tous les services, exécutez la commande suivante :


`docker-compose up --build`
Cette commande va construire les images Docker pour le script ETL et PostgreSQL.


Lancer les conteneurs pour PostgreSQL, le script ETL, et Metabase.

## **Explication du Processus ETL**

1. **Extraction des Données**
Les fichiers CSV doivent être placés dans le dossier data/. Le script Python dans src/loader_script.py lira ces fichiers et commencera le processus d'extraction des données.

2. **Transformation des Données**
Des transformations sont appliquées pour nettoyer et enrichir les données avant de les charger dans la base de données. Voici quelques transformations effectuées :

* **Gestion des valeurs manquantes** : Remplacement des valeurs nulles par des valeurs par défaut, telles que 0 pour CustomerID et Unknown pour Description.
* **Ajout de colonnes calculées** : Création d'une colonne Total, qui est le produit de Quantity et UnitPrice.
* **Filtrage des données** : Suppression des lignes avec des valeurs UnitPrice nulles ou négatives.
* **Types de données** : Conversion de certaines colonnes pour correspondre aux types requis par PostgreSQL.
Ces transformations permettent de garantir la qualité des données et de préparer celles-ci pour des analyses plus précises.

3. **Chargement des Données**
Les données transformées sont ensuite chargées dans deux tables :

La table originale Retail, qui contient les données brutes extraites du CSV.
La table Retail_transformed, qui contient les données après transformation.
Chaque table est créée automatiquement par le script ETL si elle n'existe pas déjà.

## **Accès à Metabase**
Une fois les conteneurs lancés, vous pouvez accéder à Metabase pour explorer les données. Allez à l’adresse suivante dans votre navigateur :

http://localhost:3000

Lors de la première connexion, vous devrez configurer un compte Metabase. Une fois configuré, vous pourrez interroger et visualiser les données chargées dans PostgreSQL.

## **Structure du Projet**
* data/ : Contient le fichier CSV d'entrée.
* src/loader_script.py : Script Python pour le pipeline ETL.
* Dockerfile : Configuration pour créer une image Docker pour le script ETL.
* docker-compose.yml : Fichier de configuration Docker Compose pour orchestrer les services.
* README.md : Documentation du projet.

## Exemple de Commandes Utiles
Pour relancer uniquement le service loader :

`docker-compose up --build loader`

Pour voir les logs d’un service (par exemple, le loader) :

`docker-compose logs loader`

Pour arrêter tous les services :

`docker-compose down`

## Améliorations Possibles
Automatisation des transformations avancées : Ajouter plus de transformations pour analyser les données et générer des statistiques.
Ajout de tests automatisés : Créer des tests pour vérifier que les données sont bien transformées avant d'être chargées.
Support multi-fichiers : Adapter le script ETL pour gérer automatiquement plusieurs types de fichiers de données.

N'hésitez pas à contribuer ou à soumettre des issues pour améliorer ce projet. Ce projet est conçu pour illustrer comment un pipeline ETL peut être mis en œuvre en utilisant une architecture Dockerisée avec PostgreSQL et Metabase.