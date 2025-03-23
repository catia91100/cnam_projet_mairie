# Étape 1 : Construction de l'application avec toutes les dépendances
FROM node:18-alpine AS builder

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie uniquement les fichiers nécessaires pour l'installation des dépendances
COPY package.json package-lock.json ./

# Installation des dépendances en mode production
RUN npm install

# Copie le reste du code source dans le conteneur
COPY . .

# Construire l'application Next.js avec affichage détaillé des logs
RUN npm run build --verbose

# Étape 2 : Création d'une image légère pour l'exécution de l'application
FROM node:18-alpine

WORKDIR /app

# Copier uniquement les fichiers nécessaires depuis l'étape de build
COPY --from=builder /app ./

# Installation des dépendances de production seulement
RUN npm install --production

# Expose le port utilisé par Next.js
EXPOSE 3000

# Commande pour démarrer l'application en mode production
CMD ["npm", "run", "start"]
