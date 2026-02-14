# Incident Management System v2

Flask + PostgreSQL (WSL) + Minikube Kubernetes + Docker + GitHub Actions
CI/CD

------------------------------------------------------------------------

## Project Overview

This project demonstrates a production-style DevOps workflow including:

-   Flask Web Application
-   PostgreSQL Database (running in WSL)
-   Kubernetes Deployment (Minikube)
-   Docker Image Build & Push
-   GitHub Actions CI Pipeline
-   DockerHub Image Registry
-   Horizontal Pod Autoscaler (HPA)
-   Liveness & Readiness Probes
-   Authentication & Role-Based Access Control (RBAC)
-   REST API alongside UI

------------------------------------------------------------------------

## Architecture Flow

Code Push → GitHub → GitHub Actions (CI) → DockerHub → Minikube (CD) →
Pod → Browser

CI runs in GitHub cloud. CD runs locally inside Minikube cluster.

------------------------------------------------------------------------

## Technology Stack

Application Layer: - Flask - Flask-Login - SQLAlchemy - bcrypt

Infrastructure Layer: - Docker - Kubernetes (Minikube) - PostgreSQL
(WSL)

DevOps Layer: - GitHub Actions - DockerHub Registry - HPA

------------------------------------------------------------------------

## Machine Setup Requirements

### Windows + WSL2

Verify:

    wsl --status

### Docker Desktop

Verify:

    docker version

### Minikube

Start:

    minikube start --driver=docker

Enable metrics:

    minikube addons enable metrics-server

### PostgreSQL (WSL)

Install:

    sudo apt update
    sudo apt install postgresql postgresql-contrib -y
    sudo service postgresql start

------------------------------------------------------------------------

## Database Setup

    sudo -i -u postgres
    psql
    CREATE USER devuser WITH PASSWORD 'devpassword';
    CREATE DATABASE devdb OWNER devuser;
    GRANT ALL PRIVILEGES ON DATABASE devdb TO devuser;
    \q
    exit

Run schema:

    psql -U devuser -d devdb -f db/schema.sql

------------------------------------------------------------------------

## Authentication Setup

Generate bcrypt hash:

    python3

    import bcrypt
    print(bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode())

Insert admin user:

    INSERT INTO devops_app.users (username,password_hash,role)
    VALUES ('admin','<hashed_password>','admin');

------------------------------------------------------------------------

## CI/CD Setup

### Create DockerHub Repo

Repository name: incident-mgmt-v2 Make it Public.

### Add GitHub Secrets

Repository → Settings → Secrets → Actions

Add: DOCKER_USERNAME = your DockerHub username DOCKER_PASSWORD =
DockerHub Access Token

------------------------------------------------------------------------

## Kubernetes Deployment

Ensure deployment.yaml image:

    image: <dockerhub-username>/incident-mgmt-v2:latest
    imagePullPolicy: Always

Deploy:

    kubectl apply -f k8s/
    kubectl rollout restart deployment flask-app

------------------------------------------------------------------------

## Access Application

    kubectl port-forward service/flask-service 9090:80

Open: http://localhost:9090/login

------------------------------------------------------------------------

## REST API

GET: /api/incidents

POST: /api/incidents

Example JSON: { "title": "Database Issue", "description": "High latency
observed" }

------------------------------------------------------------------------

## HPA

Apply:

    kubectl apply -f k8s/hpa.yaml

Check:

    kubectl get hpa

------------------------------------------------------------------------

## Troubleshooting

ImagePullBackOff: - Verify DockerHub repo exists - Verify image tag
exists - Verify repo visibility

Check logs:

    kubectl logs <pod-name>

------------------------------------------------------------------------

## Deployment Flow Summary

1.  Push code to GitHub
2.  GitHub builds Docker image
3.  Image pushed to DockerHub
4.  Kubernetes pulls image
5.  Pod runs app
6.  Browser accesses service

------------------------------------------------------------------------

## Future Enhancements

-   JWT Authentication
-   Ingress + TLS
-   Prometheus Monitoring
-   ArgoCD GitOps
-   StatefulSet Database
