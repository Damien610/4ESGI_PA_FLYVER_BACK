#!/bin/sh

# Vérifie que les variables d'environnement sont bien définies
: "${DB_HOST:?Variable DB_HOST non définie}"
: "${DB_PORT:?Variable DB_PORT non définie}"

echo "⏳ Attente de SQL Server (${DB_HOST}:${DB_PORT})..."

# Attente active jusqu'à ce que le port de la DB soit ouvert
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "✅ SQL Server est prêt. Lancement de l'application..."

# Exécute la commande passée (ex: uvicorn main:app --host 0.0.0.0 --port 8000)
exec "$@"
