#!/bin/sh

echo "⏳ Waiting for SQL Server to be ready..."

until nc -z -v -w30 sqlserver 1433
do
  echo "🕓 SQL Server not ready, waiting..."
  sleep 2
done

echo "📁 Files in /app:"
ls /app

echo "✅ SQL Server is up! Starting FastAPI..."

# 👇 Change ici si ton main.py est dans un dossier
exec uvicorn main:app --host 0.0.0.0 --port 8000

