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

# Initialisation Terraform si main.tf est présent
if [ -f "/app/main.tf" ]; then
  echo "🔧 Initialisation de Terraform..."
  terraform -chdir=/app init
  echo "🔧 Application de la configuration Terraform..."
  terraform -chdir=/app apply -auto-approve
else
  echo "⚠️ Aucun fichier main.tf trouvé, Terraform ignoré."
fi

# Exécute la commande passée (ex: uvicorn ...)
exec "$@"
