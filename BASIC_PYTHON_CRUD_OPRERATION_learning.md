# BASIC_PYTHON_CRUD_OPERATION_learning

This guide explains how to set up Python and MongoDB Compass in this workspace, how the project works end-to-end, and the full execution flow for a beginner.

## 1. Install Python on Windows

1. Download Python:
   - Go to https://www.python.org/downloads/windows/
   - Choose the latest stable release, such as Python 3.14.x.

2. Run the installer:
   - Check `Add Python to PATH`.
   - Choose `Install Now` or `Customize installation` and keep defaults.

3. Verify the installation in PowerShell:

   ```powershell
   python --version
   pip --version
   ```

4. Create a project workspace folder:
   - Use your existing workspace: `c:\Users\rajekuma\Documents\AI-Learning\AI-AGENT-ALL`

## 2. Set up the Python virtual environment in this workspace

1. Open a PowerShell terminal in the workspace.
2. Create the virtual environment:
   ```powershell
   python -m venv venv
   ```
3. Activate the environment:
   ```powershell
   venv\Scripts\activate.bat
   ```
4. Install dependencies:
   ```powershell
   venv\Scripts\pip install -r requirements.txt
   ```

## 3. What this project contains

The workspace now includes a complete Python backend sample:

- `raraphsopvt/` package
  - `main.py` - FastAPI app factory
  - `api.py` - service routes and endpoints
  - `service.py` - business rules and validation
  - `repository.py` - SQLite repository layer
  - `config.py` - environment configuration
  - `logging_config.py` - logger setup with file + console output
  - `exceptions.py` - global app exception classes
  - `security.py` - HTTP Bearer token authentication
  - `schemas.py` - request and response payload models

- `tests/` - pytest test suite for the repository, service, and HTTP API
- `mongo_sample.py` - MongoDB CRUD example for MongoDB Compass and Python integration
- `.env` - local configuration for API key, database URLs, and MongoDB

## 4. Configure MongoDB Compass with this workspace

MongoDB Compass is a GUI tool for inspecting MongoDB databases.

### Install MongoDB Compass

1. Download Compass:
   - Go to https://www.mongodb.com/try/download/compass
   - Select the Windows installer.
2. Install it using the downloaded installer.
3. Launch MongoDB Compass after installation.

### Configure MongoDB Compass

1. Use the default connection string for a local MongoDB server:
   - `mongodb://localhost:27017`
2. If you are using Atlas or another cluster, copy the connection string from Atlas.
3. Paste the connection string into Compass and connect.
4. Create or select the database named `raraphsopvt`.
5. Create the collection named `tasks`.

### Connect Python to MongoDB

The project uses environment variables in `.env`:

- `MONGODB_URI` - MongoDB connection URL
- `MONGODB_DB` - database name (`raraphsopvt`)

Example values in `.env`:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=raraphsopvt
```

## 5. MongoDB sample script

The file `mongo_sample.py` shows how to:

- connect to MongoDB
- create a task document
- read it back
- update a task
- delete a task
- list all tasks

Run it with the virtual environment activated:

```powershell
venv\Scripts\python mongo_sample.py
```

## 6. Python execution flow end to end

This section explains how a request flows through the sample backend.

### 6.1 Start the app

Run the backend with Uvicorn:

```powershell
venv\Scripts\python -m uvicorn raraphsopvt.main:app --reload
```

- Uvicorn starts the ASGI server.
- FastAPI creates the app from `raraphsopvt.main:create_app()`.
- The app loads configuration from `.env` via `raraphsopvt.config`.
- `raraphsopvt.logging_config` initializes logging.
- `raraphsopvt.main` includes the API router and sets up global exception handling.

### 6.2 Incoming request flow

1. **Client request arrives**
   - Example: `POST /api/v1/tasks/` with JSON payload.

2. **FastAPI routing**
   - The route is defined in `raraphsopvt.api`.
   - Each route has dependency injection for authentication.

3. **Security check**
   - `raraphsopvt.security.get_api_key()` validates the Bearer token.
   - If the token is invalid, a 401 error is returned.

4. **API layer**
   - The route handler receives a Pydantic model (`TaskCreate`, `TaskUpdate`).
   - Request payload is validated automatically.
   - The handler forwards the request to `TaskService`.

5. **Service layer**
   - `raraphsopvt.service.TaskService` contains business rules.
   - It validates data and converts a request into repository calls.
   - If the resource is missing, it raises a custom exception.

6. **Repository layer**
   - `raraphsopvt.repository.TaskRepository` performs data access.
   - SQLite is used for the default implementation.
   - For MongoDB, `mongo_sample.py` demonstrates the equivalent CRUD logic.

7. **Response creation**
   - The service returns a response model.
   - FastAPI serializes it to JSON and sends it back to the client.

8. **Global exception handling**
   - `raraphsopvt.main` catches `AppException` and returns a structured error.
   - Any other exception returns a generic 500 internal server error.

9. **Logging**
   - The app logs request lifecycle events and errors.
   - Logs are written to both console and `app.log`.

## 7. Basic CRUD operations in Python

### Create

1. Validate the incoming payload.
2. Insert a new record into the database.
3. Return the saved record.

### Read

1. Find a record by ID.
2. If not found, raise a `NotFoundException`.
3. Return the record data.

### Update

1. Validate partial update payload.
2. Merge existing values with updated values.
3. Persist the changes.
4. Return the updated record.

### Delete

1. Delete the record by ID.
2. Return a success response if deletion succeeds.
3. If the record does not exist, raise a `NotFoundException`.

## 8. How to inspect MongoDB data in Compass

1. Open MongoDB Compass.
2. Connect to the same URI used by Python.
3. Navigate to `raraphsopvt` database.
4. Open the `tasks` collection.
5. Review inserted documents and fields.

## 9. Summary of commands

```powershell
# activate venv
venv\Scripts\activate.bat

# install dependencies
venv\Scripts\pip install -r requirements.txt

# run the FastAPI app
venv\Scripts\python -m uvicorn raraphsopvt.main:app --reload

# run the MongoDB sample script
venv\Scripts\python mongo_sample.py

# run tests
venv\Scripts\pytest -q
```
