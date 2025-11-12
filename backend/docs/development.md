# Development Guide

## Overview

This document provides instructions for setting up and developing the LADR English backend application.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Virtual environment tool (optional but recommended)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ladr-english/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

## Project Structure

The project follows a layered architecture:

```
app/
├── api/              # API endpoints
├── core/             # Core configuration and utilities
├── models/           # Database models
├── repositories/     # Data access layer
├── schemas/          # Pydantic models
├── services/         # Business logic
└── utils/            # Utility functions
```

## Development Commands

### Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using the Makefile:
```bash
make run
```

### Run Tests

```bash
pytest tests/ -v
```

Or using the Makefile:
```bash
make test
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

Or using the Makefile:
```bash
make coverage
```

## Code Quality

### Formatting

The project uses Black for code formatting:
```bash
black .
```

### Linting

The project uses Flake8 for linting:
```bash
flake8 .
```

## Database

The application uses SQLAlchemy as the ORM. Database migrations are handled manually for now.

## API Documentation

The API is documented using the OpenAPI standard. Access the documentation at:
- `/docs`: Swagger UI
- `/redoc`: ReDoc

## Testing

Tests are written using pytest. Test files are located in the `tests/` directory.

### Test Structure

```
tests/
├── unit/         # Unit tests
├── integration/  # Integration tests
└── e2e/          # End-to-end tests
```

## Deployment

See the [Deployment Guide](deployment.md) for deployment instructions.