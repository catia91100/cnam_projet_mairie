# Utilisation de l'image Python basée sur Alpine
FROM python:3.11-alpine

# Définir un utilisateur non-root pour la sécurité
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie uniquement le fichier des dépendances d'abord pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances sans conserver les fichiers temporaires
RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copier le reste du code après l'installation des dépendances
COPY . .

# Changer les permissions pour le user sécurisé
RUN chown -R appuser:appgroup /app

# Passer en utilisateur non-root
USER appuser

# Exposer le port de l’API Flask
EXPOSE 5000

# Commande pour démarrer Flask en production avec Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
# Définir la commande par défaut pour exécuter l'application avec Gunicorn
# CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]