# Backend Developer Technical Assessment

## Overview

This project implements a simple data pipeline using Docker, Flask, FastAPI, and PostgreSQL.

### Architecture

```text
Flask Mock API (Port 5000)
          │
          ▼
FastAPI Ingestion Service (Port 8000)
          │
          ▼
PostgreSQL Database (Port 5432)
```

### Data Flow

```text
customers.json
      │
      ▼
Flask API
      │
      ▼
FastAPI Ingestion Endpoint
      │
      ▼
PostgreSQL Customers Table
      │
      ▼
Customer Query APIs
```

---

# Project Structure

```text
project-root/
│
├── docker-compose.yml
├── README.md
│
├── mock-server/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── data/
│       └── customers.json
│
└── pipeline-service/
    ├── main.py
    ├── database.py
    ├── requirements.txt
    ├── Dockerfile
    │
    ├── models/
    │   └── customer.py
    │
    └── services/
        └── ingestion.py
```

---

# Technologies Used

* Python 3.11
* Flask
* FastAPI
* PostgreSQL 15
* SQLAlchemy
* Requests
* Docker
* Docker Compose
* dlt

---

# Prerequisites

Ensure the following are installed:

* Docker Desktop
* Docker Compose
* Python 3.10+

Verify Docker Compose:

```bash
docker-compose --version
```

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
cd project-root
```

---

## Build and Start Services

```bash
docker-compose up --build
```

Run in detached mode:

```bash
docker-compose up -d --build
```

---

## Verify Running Containers

```bash
docker ps
```

Expected containers:

* postgres
* mock-server
* pipeline-service

---

# API Endpoints

## Flask Mock Server

Base URL:

```text
http://localhost:5000
```

### Health Check

```http
GET /api/health
```

Response:

```json
{
  "status": "healthy"
}
```

---

### Get Customers

```http
GET /api/customers?page=1&limit=5
```

Response:

```json
{
  "data": [],
  "total": 20,
  "page": 1,
  "limit": 5
}
```

---

### Get Customer By ID

```http
GET /api/customers/CUST001
```

Response:

```json
{
  "customer_id": "CUST001",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

## FastAPI Pipeline Service

Base URL:

```text
http://localhost:8000
```

---

### Ingest Data

Fetches all customers from the Flask API and stores them in PostgreSQL.

```http
POST /api/ingest
```

Response:

```json
{
  "status": "success",
  "records_processed": 20
}
```

---

### Get Customers From Database

```http
GET /api/customers?page=1&limit=5
```

Response:

```json
{
  "data": [],
  "total": 20,
  "page": 1,
  "limit": 5
}
```

---

### Get Customer By ID

```http
GET /api/customers/CUST001
```

Response:

```json
{
  "customer_id": "CUST001",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

# Database Schema

Table: customers

| Column          | Type                    |
| --------------- | ----------------------- |
| customer_id     | VARCHAR(50) PRIMARY KEY |
| first_name      | VARCHAR(100)            |
| last_name       | VARCHAR(100)            |
| email           | VARCHAR(255)            |
| phone           | VARCHAR(20)             |
| address         | TEXT                    |
| date_of_birth   | DATE                    |
| account_balance | DECIMAL(15,2)           |
| created_at      | TIMESTAMP               |

---

# Testing

## Test Flask API

```bash
curl http://localhost:5000/api/customers?page=1&limit=5
```

---

## Test Health Endpoint

```bash
curl http://localhost:5000/api/health
```

---

## Ingest Data

```bash
curl -X POST http://localhost:8000/api/ingest
```

Expected output:

```json
{
  "status": "success",
  "records_processed": 20
}
```

---

## Query Database Records

```bash
curl http://localhost:8000/api/customers?page=1&limit=5
```

---

## Get Single Customer

```bash
curl http://localhost:8000/api/customers/CUST001
```

---

# Features Implemented

### Flask Mock Server

* Loads customer data from JSON file
* Pagination support
* Single customer retrieval
* Health check endpoint
* Proper 404 handling
* Dockerized deployment

### FastAPI Pipeline

* Fetches paginated data automatically
* SQLAlchemy ORM integration
* PostgreSQL persistence
* Upsert support
* Pagination support
* Single customer retrieval
* Error handling
* Dockerized deployment

### Infrastructure

* Docker Compose orchestration
* PostgreSQL database container
* Service-to-service communication
* Environment variable configuration

---

# Future Improvements

* Full dlt pipeline integration
* Alembic database migrations
* Automated unit tests
* Structured logging
* Retry mechanisms for ingestion failures
* API authentication and authorization

---

# Author

Charan Kandimalla

Backend Developer Technical Assessment Submission
