# Utilisation d'une image Node.js optimisée pour la production
FROM node:18-alpine AS builder

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie uniquement les fichiers nécessaires pour l'installation des dépendances
COPY package.json package-lock.json ./

# Installation des dépendances en mode production
RUN npm install --only=production

# Copie le reste du code source dans le conteneur
COPY . .

# Construire l'application Next.js
RUN npm run build

# Étape finale : création d'une image légère pour exécuter l'application
FROM node:18-alpine

WORKDIR /app

# Copier uniquement les fichiers nécessaires depuis l'étape de build
COPY --from=builder /app ./

# Expose le port utilisé par Next.js
EXPOSE 3000

# Commande pour démarrer l'application en mode production
CMD ["npm", "run", "start"]
