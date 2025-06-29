#!/bin/sh

# Attendre que MinIO soit prêt
sleep 5

# Configurer l'alias local
mc alias set local http://minio:9000 minioadmin minioadmin

# Créer le bucket s'il n'existe pas
mc mb --ignore-existing local/images;


# Appliquer la policy publique
mc policy set public local/images
