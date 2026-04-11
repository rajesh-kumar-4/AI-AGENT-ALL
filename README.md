# RaraphSOPVT Python Backend Sample

This workspace contains a beginner-friendly Python backend sample project for `raraphsopvt`.
It includes:

- FastAPI REST API with full CRUD for a task resource
- Repository and service layers
- Global exception handling
- Logging and configuration
- API security via Bearer token
- Sample tests using `pytest`

## Project structure

- `raraphsopvt/` - application package
  - `api.py` - REST routing
  - `service.py` - business logic
  - `repository.py` - data access layer using SQLite
  - `schemas.py` - request and response models
  - `security.py` - API authentication
  - `exceptions.py` - application exceptions and handlers
  - `logging_config.py` - shared logger setup
  - `config.py` - environment settings
  - `main.py` - FastAPI application factory

- `tests/` - test suite for repository, service, and API flows
- `mongo_sample.py` - MongoDB Compass sample script for Python CRUD
- `BASIC_PYTHON_CRUD_OPRERATION_learning.md` - step-by-step Python and MongoDB Compass tutorial

## Setup

1. Activate the virtual environment:

   ```powershell
   venv\Scripts\activate.bat
   ```

2. Install dependencies (if needed):

   ```powershell
   venv\Scripts\pip install -r requirements.txt
   ```

3. Run the app:

   ```powershell
   venv\Scripts\python -m uvicorn raraphsopvt.main:app --reload
   ```

4. Use the Bearer token from `.env`:
   - `supersecretkey`

## API endpoints

- `GET /api/v1/tasks/`
- `POST /api/v1/tasks/`
- `GET /api/v1/tasks/{task_id}`
- `PUT /api/v1/tasks/{task_id}`
- `DELETE /api/v1/tasks/{task_id}`

## Tests

Run:

```powershell
venv\Scripts\pytest -q
```
