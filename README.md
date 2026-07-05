# AI Recruitment Platform with DevSecOps

## Overview

This repository contains a full-stack recruitment platform designed to streamline hiring workflows through a modern web interface, AI-assisted resume evaluation, and container-based deployment practices. The project combines a React frontend, a FastAPI backend, and PostgreSQL persistence to support job posting, candidate intake, resume scoring, and recruiter-facing insights.

The solution is also structured as a DevSecOps-oriented sample application, with Docker and Kubernetes deployment assets, monitoring configuration, and security scanning scripts included in the repository.

## What the Project Does

The platform currently supports the following capabilities:

- Recruiter-facing workflows for creating job descriptions and managing candidates
- Candidate-facing job browsing through a simple portal experience
- Resume upload and storage
- AI-based resume scoring against required job skills
- Candidate matching insights, including matched and missing skills
- Authentication endpoints for recruiter signup and login
- Containerized deployment using Docker Compose and Kubernetes manifests
- Monitoring and security scanning assets for operational readiness

## Architecture

The application is organized as a layered full-stack system:

- Frontend: React + Vite for the user experience
- Backend: FastAPI for API endpoints and business logic
- Database: PostgreSQL for jobs, candidates, and recruiter records
- File handling: Uploaded resumes are stored on disk for processing
- DevSecOps assets: Docker, Kubernetes, Prometheus/Grafana templates, and Trivy-based security scanning

## Technology Stack

### Frontend
- React
- Vite
- React Router
- Axios

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT-based authentication
- Python file upload and PDF text extraction

### DevSecOps and Deployment
- Docker
- Docker Compose
- Kubernetes manifests
- Prometheus and Grafana configuration examples
- Trivy security scan script

## Project Structure

```text
backend/           # FastAPI application, routes, services, and models
frontend/          # React/Vite client application
database/          # SQL initialization files
docs/              # Architecture and pipeline diagrams
kubernetes/        # Kubernetes deployment manifests
monitoring/        # Prometheus and Grafana-related assets
security/          # Security scanning and secret examples
docker-compose.yml # Local multi-container orchestration
```

## Prerequisites

Before running the project locally, ensure the following tools are installed:

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL (if running outside containerized setup)

## Getting Started

### Option 1: Run with Docker Compose

From the repository root, start the application stack:

```bash
docker compose up --build
```

This will start:

- Frontend on http://localhost:5173
- Backend on http://localhost:8000
- PostgreSQL on localhost:5432

The backend API documentation is available at:

- http://localhost:8000/docs

### Option 2: Run the Services Locally

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

> Note: The current backend uses a PostgreSQL connection string defined in the backend configuration. If you run the services outside the provided container setup, ensure the database is reachable and the connection settings match your environment.

## Key API Capabilities

The backend exposes routes for:

- Job management: create and list jobs
- Resume upload and scoring
- Candidate listing and filtering
- Candidate analytics and insights
- Recruiter authentication and signup

## Security and DevSecOps Notes

The repository includes several security and operational assets:

- A Trivy-based scan script in the security folder
- Example secret environment configuration
- Kubernetes deployment manifests for service-oriented deployment
- Monitoring configuration placeholders for Prometheus and Grafana

These assets provide a foundation for secure deployment practices and observability, although they should be adapted to your environment and compliance requirements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
