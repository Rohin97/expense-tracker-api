## Expense Tracker API

A **production-ready fintech backend API** for expense tracking.
Built with **Django REST Framework, JWT authentication, PostgreSQL, and Docker**, this service enables multi-user expense management and can be integrated into other applications or used as a standalone API.

## Features

User registration & authentication with JWT tokens

CRUD endpoints for expenses

Category-based expense tracking

PostgreSQL database (with Docker persistence)

Containerized deployment with Docker + Docker Compose

Cloud-ready (tested on Render)

## Tech Stack

Backend: Python, Django, Django REST Framework

Auth: JWT (djangorestframework-simplejwt)

Database: PostgreSQL

Deployment: Docker, Render

Testing: Pytest

## Setup & Installation

Clone the repo:

git clone https://github.com/<your-username>/expense-tracker-api.git
cd expense-tracker-api

1. Environment

Create a .env file and set:

SECRET_KEY=your-secret-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://expense_user:expense_pass@db:5432/expense_db

2. Run with Docker
docker compose up --build


The API will be available at:
http://localhost:8000

3. Run locally (without Docker)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

**Note: Available test users with data.**
1. 
{
  "username": "ashley",
  "password": "ashleyashley"
}

2.
{
  "username": "bobby",
  "password": "bobbybobby"
}

## Authentication Endpoints

All protected endpoints require JWT auth.

Register a user:

POST /api/auth/register/
Content-Type: application/json

{
  "username": "ashley",
  "password": "ashleyashley"
}


Obtain a token:

POST /api/auth/token/
{
  "username": "ashley",
  "password": "ashleyashley"
}


Response:

{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "..."
}


Use the token:

Authorization: Bearer <access_token>

## Expenses API Endpoints

GET /api/expenses/ → list all expenses for the logged-in user

POST /api/expenses/ → create a new expense

{
  "description": "Lunch",
  "category": "food",
  "amount": "12.50"
}

GET /api/expenses/<id>/ → get an expense

PATCH /api/expenses/<id>/ → update an expense

DELETE /api/expenses/<id>/ → delete an expense

GET /api/expenses/summary/ → monthly totals by category

## Authentication (via cURL)

Register a user
curl -X POST https://your-service.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bobby",
    "password": "bobbybobby"
  }'

Obtain JWT tokens
curl -X POST https://your-service.onrender.com/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bobby",
    "password": "bobbybobby"
  }'


Response:

{
  "access": "eyJhbGciOiJIUzI1NiIsInR...",
  "refresh": "..."
}

## Expenses API (cURL Examples)
Create an expense
curl -X POST https://your-service.onrender.com/api/expenses/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Lunch",
    "category": "food",
    "amount": "12.50"
  }'

List expenses
curl -X GET https://your-service.onrender.com/api/expenses/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

Update an expense
curl -X PATCH https://your-service.onrender.com/api/expenses/1/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "15.75"
  }'

Delete an expense
curl -X DELETE https://your-service.onrender.com/api/expenses/1/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

Get summary
curl -X GET https://your-service.onrender.com/api/expenses/summary/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

## Testing

Run tests with:

docker compose exec web pytest -q

## Postman Collection

This repo includes a **Postman collection** so you can explore the API quickly.

- File: [`postman/Expense-Tracker-API.postman_collection.json`](postman/Expense-Tracker-API.postman_collection.json)  
- Import it into Postman:
  1. Open Postman → File → Import
  2. Choose the JSON file
  3. Set the `{{base_url}}` environment variable:
     - Locally: `http://localhost:8000`
     - On Render: `[https://expense-tracker-api-b2l4.onrender.com](https://expense-tracker-api-b2l4.onrender.com/)`

The collection covers:
- User registration & login
- Token refresh
- CRUD for expenses
- Summary endpoint
