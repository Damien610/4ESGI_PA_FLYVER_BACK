# FLYVER_BACK

## lancer l'API Flyver
```bash
docker-compose up  --build
```

## Accéder à l'API
L'API est accessible à l'adresse suivante : [http://localhost:8000](http://localhost:8000)

## Documentation de l'API
La documentation de l'API est disponible à l'adresse suivante : [http://localhost:8000/docs](http://localhost:8000/docs)

## Développement de l'API
Pour développer l'API, vous pouvez modifier les fichiers dans le dossier `app`. Les fichiers sont organisés de la manière suivante :
- `app/main.py` : Point d'entrée de l'application FastAPI.
- `app/api/` : Contient les routes de l'API.
- `app/models/` : Contient les modèles de données utilisés par l'API.
- `app/schemas/` : Contient les schémas de validation des données.
- `app/core/` : Contient la configuration de l'application et les dépendances.
- `app/utils/` : Contient les fonctions utilitaires de l'application.

## Utilisation de l'API
Pour utiliser l'API, vous pouvez envoyer des requêtes HTTP à l'API en utilisant un client HTTP comme Postman ou curl. Vous pouvez également utiliser la documentation interactive de l'API disponible à l'adresse [http://localhost:8000/docs](http://localhost:8000/docs) pour tester les différentes routes de l'API.
Atention, l'API est en mode développement, ce qui signifie que les modifications apportées au code seront automatiquement rechargées sans avoir besoin de redémarrer le serveur.
Certaines routes de l'API nécessitent une authentification. Vous pouvez vous authentifier en utilisant le token JWT généré lors de la connexion. Pour plus d'informations sur l'authentification, consultez la documentation de l'API.

## Modification du code du dossier `models`
Toute modification du code dans le dossier `models` nécessite de reconstruire l'image Docker pour que les modifications soient prises en compte. Vous pouvez le faire en exécutant la commande suivante :
```bash
docker-compose down -v
docker-compose up --build
```