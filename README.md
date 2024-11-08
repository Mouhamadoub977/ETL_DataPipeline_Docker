# Title 
Implementing ETL data pipeline using docker project.

## Pre-requisite

To run the code, you will need:  
- Docker and Docker Compose
- git

# Architecture: 

[alt text](architecture.webp)

# Objectif:

Ce projet implémente un pipeline ETL simple permettant d'extraire des données à partir de fichiers CSV, de les transformer et de les charger dans une base de données PostgreSQL en tant que système de data warehouse. Après avoir stocké les données, celles-ci sont mises à la disposition des utilisateurs finaux via Metabase, qui offre des fonctionnalités d'exploration et de visualisation des données.

# Steps:
- Alimentez le dossier data avec un fichier de données au format CSV.

- Modifiez le fichier src/loader/loader_script.py en intégrant le script ETL du précédent projet. Ce script devra extraire, transformer et charger les données dans la base de données PostgreSQL.

- Complétez le Dockerfile existant situé dans /containers/loader/Dockerfile. Ce fichier doit permettre de créer une image personnalisée pour votre script Python (ETL), les dépendances nécessaire pour l'exécuter, ainsi que le client postgres pour connecter à la BD. Vous pouvez ajouter la commande "tail -f /dev/null" à la fin du Dockerfile pour maintenir le conteneur actif.

- Après avoir créé l'image, mettez à jour le fichier docker-compose.yml en spécifiant le nom de l'image créée dans la section loader.

- Une fois toutes les étapes précédentes terminées, lancez les conteneurs et exécutez le traitement ETL. Pour cela, vous pouvez consulter les commandes dans le fichier Makefile.

- Enfin, connectez-vous à Metabase pour visualiser les modifications apportées à la base de données sur http://localhost:3000.