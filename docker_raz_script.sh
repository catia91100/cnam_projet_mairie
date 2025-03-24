#!/bin/bash

# Supprimer tous les conteneurs arrêtés
echo "Suppression des conteneurs arrêtés..."
docker container prune -f

# Supprimer toutes les images non utilisées
echo "Suppression des images non utilisées..."
docker image prune -a -f

# Supprimer tous les volumes non utilisés
echo "Suppression des volumes non utilisés..."
docker volume prune -f

# Supprimer tous les réseaux non utilisés
echo "Suppression des réseaux non utilisés..."
docker network prune -f

echo "Nettoyage Docker terminé !"
# docker-compose up --build
