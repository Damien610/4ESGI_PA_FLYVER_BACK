# ✈️ Flyver API — Backend FastAPI

Back-end de l'application **Flyver**, développé en **Python avec FastAPI**, destiné à gérer les opérations métiers autour des aéroports, vols, avions, passagers et réservations. Ce service inclut également un système de stockage d'images avec **MinIO** et une base de données **SQL Server**, le tout orchestré via Docker Compose.

---

## 📁 Structure du projet

Le code source de l'API se trouve dans le dossier `app/`, organisé de la manière suivante :

```
app/
├── api/         # Définition des routes FastAPI
├── core/        # Configuration de l’application, dépendances
├── models/      # Modèles SQLModel (base de données)
├── schemas/     # Schémas Pydantic (validation données)
├── utils/       # Fonctions utilitaires (hashing, fichiers, etc.)
├── main.py      # Point d'entrée de l'application FastAPI
```

---

## ⚙️ Technologies utilisées

- **FastAPI** — API moderne, rapide et asynchrone
- **SQLModel** — ORM basé sur SQLAlchemy + Pydantic
- **SQL Server** — Base de données relationnelle
- **MinIO** — Stockage objet (images des aéroports)
- **Docker / Docker Compose** — Conteneurisation de l’ensemble des services
- **Pytest** — Tests unitaires

---

## 🚀 Lancer le projet en local

### Prérequis

- Docker & Docker Compose installés

### Lancer les services

```bash
docker-compose up --build
```

Cela démarre :
- L’API FastAPI (port `8000`)
- La base de données SQL Server (port `1433`)
- Le service MinIO (port `9000`)

### Accéder à l'API

- Documentation Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)
- MinIO Console : [http://localhost:9000](http://localhost:9000)

---

## 🔐 Fonctionnalités principales

- Authentification (utilisateurs, admins)
- CRUD complet :
  - Aéroports (avec upload d’images)
  - Avions, modèles d’avions
  - Vols, réservations, passagers
- Gestion des fichiers via MinIO (upload, lecture)
- Relations complexes : vols entre aéroports, réservations liées à passagers

---

## 🗃️ Modèle de données

Le projet utilise des modèles relationnels (SQLModel). Voici les entités principales :

- `Airport`
- `Flight`
- `Plane`
- `ModelPlane`
- `Passenger`
- `Reservation`
- `User`

> Voir `app/models/` pour le détail.

---

## 🔁 Workflow Git

Le développement suit un **Git flow structuré** :
- Les branches de développement sont créées à partir de `develop` (`feature/nom-fonction`)
- Une fois testées localement, elles sont mergées dans `develop`
- Après validation en test, les changements sont intégrés dans `main` pour déploiement

---

## 🧪 Lancer les tests

```bash
docker exec -it <nom_du_conteneur_back> pytest
```

---

## 📦 Variables d’environnement

À définir dans un fichier `.env` ou directement dans `docker-compose.yml` :

```env
DATABASE_URL=mssql+pyodbc://username:password@db:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

---

## 👤 Auteur

Projet réalisé dans le cadre du **projet annuel 4ESGI**.  
Développé par Damien et l’équipe Flyver.

---

## 📄 Licence

Ce projet est distribué sous licence MIT — voir le fichier `LICENSE`.
