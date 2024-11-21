
# Todo Manager API

This project is a simple **Todo Manager API** built using **FastAPI** and **SQLModel** for task management. The API allows users to create, update, delete, and retrieve tasks.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [License](#license)

## Prerequisites

Before you begin, ensure that you have the following installed on your local machine:

- **Python 3.9** or higher
- **Poetry** (for dependency management and virtual environments)

You can install **Poetry** from [the official documentation](https://python-poetry.org/docs/#installation).

To check if Poetry is installed, run:

```bash
poetry --version
```

## Setup Instructions

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/finedevsam/deep-todo-app.git
cd deep-todo-app
```

### 2. Install Project Dependencies

Use **Poetry** to install the required dependencies:

```bash
poetry install
```

This will create a virtual environment and install all the necessary dependencies.

### 3. Activate the Virtual Environment

Activate the Poetry virtual environment by running:

```bash
poetry shell
```

### 4. Database Setup

This project uses **SQLite** for data storage. The database and tables will be created automatically the first time you run the application. To manually create the database, you can run:

```bash
poetry run python -m todo.db_config.create_db_and_tables
```

## Running the Application

To start the FastAPI application locally change directory to the project root, run the following command:

```bash
poetry run uvicorn main:app --reload
```

This will start the development server on `http://127.0.0.1:8000/`. You can access the OpenAPI documentation at `http://127.0.0.1:8000/docs`.

### Running with Custom Configuration (Optional)

You can configure the server port or host if needed:

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## Running Tests

The project uses **pytest** for testing. You can run the tests with the following command:

```bash
poetry run pytest
```

### Running Tests with Coverage

To run tests with code coverage, use the following command:

```bash
poetry run pytest --cov=todo
```

This will run the tests and generate a coverage report.

### Running Tests in Watch Mode

If you'd like to run the tests in watch mode (re-running the tests automatically on file changes), use:

```bash
poetry run pytest --maxfail=1 --disable-warnings -q
```

### Key Files

- **`main.py`**: Contains the FastAPI application setup and route definitions.
- **`config/db_config.py`**: Handles database configuration, including database engine setup and session management.
- **`todo/model/`**: Contains SQLModel models for database tables.
- **`todo/dtos/`**: Contains Pydantic models for data validation (e.g., `CreateTask`, `TaskPatch`).
- **`todo/handlers/`**: Contains logic for handling CRUD operations and business logic.
- **`tests/`**: Contains unit tests for API endpoints and application logic.

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for more details.
