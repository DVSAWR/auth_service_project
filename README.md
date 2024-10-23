# FastAPI Authentication Service

This project is a simple authentication service built with FastAPI, utilizing PostgreSQL for user storage and Redis for token storage.

## Features

- User registration
- User authorization
- Token-based authentication

## Technologies Used

- FastAPI
- PostgreSQL
- Redis
- JWT for token management
- Alembic for database migrations
- Docker for containerization

## Getting Started

### Prerequisites

- Docker

### Environment Variables

Create `.env` file in the root directory with the following content:

```bash
# SERVICES
JWT_EXPIRATION_MINUTES=3
ALGORITHM=HS256
SECRET_KEY=your_secret_key

# POSTGRES
POSTGRES_DB=postgres
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_URL=postgresql+asyncpg://username:password@postgres:5432/postgres
POSTGRES_URL_LOCAL=postgresql+asyncpg://username:password@localhost:5432/postgres

# REDIS
REDIS_HOST=redis
REDIS_PASSWORD=password
REDIS_URL=redis://:password@redis:6379/0
```

### Running the Application

Build and run the Docker containers:

```bash
docker-compose up --build -d
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Database Migrations

Migrations are handled with Alembic. To apply migrations, you can run:

```bash
alembic upgrade head
```
