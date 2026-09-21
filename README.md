# Task 3 - Projects & Tasks API

A RESTful Backend API built using FastAPI with PostgreSQL database integration.

## Objective

Task 3 extends the Task 2 backend API by integrating a persistent PostgreSQL database for storing users, projects, and tasks.

The main objective is to provide reliable data persistence, proper relationships between entities, CRUD operations, validation, and secure database configuration.

## Features

- User data storage
- Project data storage
- Task data storage
- Full CRUD operations
- Project-task relationships
- Foreign key constraints
- Task status validation
- Database-level validation
- Persistent data storage using PostgreSQL
- Secure database configuration using environment variables
- Interactive Swagger API documentation

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn
- psycopg2-binary
- python-dotenv

## Project Structure

task-2-backend-api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── create_tables.py
├── requirements.txt
├── .gitignore
└── README.md

## Database

This project uses PostgreSQL as the persistent database.

Database name:

`task_manager_db`

The database contains the following tables:

- `users`
- `projects`
- `tasks`

The `tasks` table has a foreign key relationship with the `projects` table.

## Database Relationships

Users → Projects → Tasks

Projects and tasks are connected using a foreign key relationship.

## Environment Configuration

Database credentials are stored in a `.env` file and are not committed to GitHub.

Example:

`DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/task_manager_db`

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

Never upload your real database password to GitHub.

## Installation

Clone the repository:

`git clone https://github.com/Gautamdutta-star/task-2-backend-api.git`

Move into the project directory:

`cd task-2-backend-api`

Create a virtual environment:

`python -m venv venv`

Activate the virtual environment on Windows:

`venv\Scripts\activate`

Install the required dependencies:

`pip install -r requirements.txt`

## Database Setup

Create a PostgreSQL database named:

`task_manager_db`

Configure the database connection inside the `.env` file.

Example:

`DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/task_manager_db`

Create the required database tables:

`python create_tables.py`

After successful execution, the following tables will be created:

- `users`
- `projects`
- `tasks`

## Run the API

Start the FastAPI development server:

`uvicorn main:app --reload`

The API will run at:

`http://127.0.0.1:8000`

## Swagger API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open:

`http://127.0.0.1:8000/docs`

Swagger can be used to test all API endpoints and CRUD operations.

## API Operations

### Users

- GET `/users`
- POST `/users`
- GET `/users/{user_id}`
- PUT `/users/{user_id}`
- DELETE `/users/{user_id}`

### Projects

- GET `/projects`
- POST `/projects`
- GET `/projects/{project_id}`
- PUT `/projects/{project_id}`
- DELETE `/projects/{project_id}`

### Tasks

- GET `/tasks`
- POST `/tasks`
- GET `/tasks/{task_id}`
- PUT `/tasks/{task_id}`
- DELETE `/tasks/{task_id}`

## Task Status Validation

Task status values are restricted to the following options:

- `todo`
- `in-progress`
- `done`

Invalid status values are rejected by API validation.

Example of a valid task:

`{"title": "Complete database integration", "project_id": 1, "status": "todo"}`

## Database-Level Validation

Database-level validation is implemented using a PostgreSQL CHECK constraint.

The `tasks` table validates the task status at the database level.

For example, an invalid value such as `invalid` is rejected by PostgreSQL.

This provides an additional layer of data integrity beyond API-level validation.

## CRUD Testing

All CRUD operations were tested using FastAPI Swagger UI.

The following operations were tested:

- Create
- Read
- Update
- Delete

Testing was performed for:

- Users
- Projects
- Tasks

## Database Validation Testing

Database validation was also tested directly using PostgreSQL.

An invalid task status was inserted intentionally to verify the database constraint.

PostgreSQL correctly rejected the invalid value using the `check_task_status` constraint.

## Security

Sensitive database credentials are not hard-coded in the source code.

The project uses environment variables through a `.env` file.

The `.env` file is excluded from Git using `.gitignore`.

The `.gitignore` file contains:

- `venv/`
- `__pycache__/`
- `.env`
- `*.pyd`

Therefore, database passwords and other sensitive configuration values are not uploaded to GitHub.

## Task 3 Architecture

Frontend → REST API → FastAPI Backend → SQLAlchemy → PostgreSQL Database

## Task 3 Deliverables

- PostgreSQL database integration
- Database models
- Database relationships
- Full CRUD operations
- API validation
- Database-level validation
- Secure environment configuration
- GitHub repository
- Demo video
- LinkedIn post

## Learning Outcomes

Through this task, the following concepts were implemented:

- PostgreSQL database integration with FastAPI
- SQLAlchemy ORM
- Database schema design
- Primary keys and foreign keys
- CRUD operations
- Data validation
- Database constraints
- Environment variables
- Secure configuration
- REST API development
- Swagger API testing

## Author

Gautam Dutta
