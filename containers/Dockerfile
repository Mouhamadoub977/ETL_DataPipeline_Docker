# Utiliser une image Python légère
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /opt/Projet_Mouha

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet
COPY . .

# Attendre que PostgreSQL soit prêt avant d'exécuter le script
CMD ["python", "src/loader_script.py"]


