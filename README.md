# EDC Immobilier App

Application de gestion immobilière composée de deux microservices REST en Python/Flask.

## Architecture

- **user-service** (port 5001) : gestion des utilisateurs
- **property-service** (port 5002) : gestion des biens immobiliers et des pièces

Les deux services communiquent entre eux via HTTP, le property-service appelle le user-service pour vérifier qu'un propriétaire existe avant de créer un bien.

## Prérequis

- Python 3.12+ (testé seulement sur python 3.12.2)
- PostgreSQL
- pip

## Installation (Linux)

### 1. Cloner le repository

```bash
git clone https://github.com/MattDff/EDC-immobilier-app.git
cd EDC-immobilier-app
```

### 2. Créer l'environnement virtuel et installer les dépendances

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurer PostgreSQL

Créer un utilisateur et les bases de données :

```bash
sudo -u postgres psql
```

```sql
CREATE USER "votre-username" WITH SUPERUSER;
ALTER USER "votre-username" WITH PASSWORD 'votre-password';
CREATE DATABASE users_db OWNER "votre-username";
CREATE DATABASE properties_db OWNER "votre-username";
\q
```

### 4. Configurer les variables d'environnement

Créer un fichier `.env` dans `user-service/` contenant :

```
DATABASE_URL=postgresql://votre-username:votre-password@localhost/users_db
FLASK_APP=run.py
PORT=5001
```

Créer un fichier `.env` dans `property-service/` contenant :

```
DATABASE_URL=postgresql://votre-username:votre-password@localhost/properties_db
FLASK_APP=run.py
PORT=5002
USER_SERVICE_URL=http://localhost:5001
```

### 5. Initialiser les bases de données

**User service :**
```bash
cd user-service
flask db upgrade
cd ..
```

**Property service :**
```bash
cd property-service
flask db upgrade
cd ..
```

## Lancer les services

Ouvrir **deux terminaux** et lancer chaque service séparément.

**Terminal 1 : user-service :**
```bash
source .venv/bin/activate
cd user-service
python run.py
```

**Terminal 2 : property-service :**
```bash
source .venv/bin/activate
cd property-service
python run.py
```

## Lancer les tests

```bash
source .venv/bin/activate

# Tests user-service
cd user-service
pytest tests/ -v
cd ..

# Tests property-service
cd property-service
pytest tests/ -v
```

---

## Endpoints

### User Service : `http://localhost:5001/api/v1`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users` | Liste tous les utilisateurs |
| GET | `/users/<id>` | Détail d'un utilisateur |
| POST | `/users` | Créer un utilisateur |
| PUT | `/users/<id>` | Modifier un utilisateur |
| DELETE | `/users/<id>` | Supprimer un utilisateur |

**Exemple : Créer un utilisateur :**
```bash
curl -X POST http://localhost:5001/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jean", "last_name": "Dupont", "birth_date": "1990-01-15"}'
```

---

### Property Service : `http://localhost:5002/api/v1`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/properties` | Liste tous les biens |
| GET | `/properties?city=Paris` | Filtrer les biens par ville |
| GET | `/properties/<id>` | Détail d'un bien (avec ses pièces) |
| POST | `/properties` | Créer un bien |
| PUT | `/properties/<id>` | Modifier un bien ⚠️ |
| DELETE | `/properties/<id>` | Supprimer un bien ⚠️ |
| GET | `/properties/<id>/rooms` | Liste les pièces d'un bien |
| GET | `/properties/<id>/rooms/<room_id>` | Détail d'une pièce |
| POST | `/properties/<id>/rooms` | Ajouter une pièce |
| PUT | `/properties/<id>/rooms/<room_id>` | Modifier une pièce ⚠️ |
| DELETE | `/properties/<id>/rooms/<room_id>` | Supprimer une pièce ⚠️ |

> ⚠️ Ces routes nécessitent le header `X-User-Id` car seul le propriétaire du bien peut modifier ou supprimer.


**Exemple 1, Créer un bien :**
```bash
curl -X POST http://localhost:5002/api/v1/properties \
  -H "Content-Type: application/json" \
  -d '{"name": "Bel Appart", "type": "apartment", "city": "Paris", "owner_id": ""}'
```

**Exemple 2, Modifier un bien (propriétaire uniquement) :**
```bash
curl -X PUT http://localhost:5002/api/v1/properties/ \
  -H "Content-Type: application/json" \
  -H "X-User-Id: " \
  -d '{"name": "Nouveau Nom"}'
```

**Exemple 3, Ajouter une pièce :**
```bash
curl -X POST http://localhost:5002/api/v1/properties//rooms \
  -H "Content-Type: application/json" \
  -d '{"name": "Salon", "area_sqm": 25.0, "description": "Grand salon lumineux"}'
```

**Exemple 4, Filtrer par ville :**
```bash
curl http://localhost:5002/api/v1/properties?city=Paris
```

---

## Stack technique

- **Langage** : Python 3.12
- **Framework** : Flask 3.0
- **ORM** : Flask-SQLAlchemy
- **Migrations** : Flask-Migrate
- **Sérialisation** : Marshmallow
- **Base de données** : PostgreSQL
- **Tests** : pytest