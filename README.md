# IAM Architecture with Flask + Keycloak

This repo contains a secure identity and access management (IAM) environment using Keycloak (OAuth 2.0) and a protected Flask microservice.

## Features

- OAuth2 + OpenID Connect with Keycloak
- JWT validation with Flask
- Dockerized setup with PostgreSQL backend
- Automated test script (`make test`)

## Usage

```bash
make reset        # Rebuild and restart everything
make test         # Test public and protected endpoints
make down         # Stop and clean everything
