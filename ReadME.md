# Task Management REST API

A RESTful API for managing tasks with full CRUD operations, filtering, sorting, and validation. Built with FastAPI and SQLite.

---

## Quick Start
```bash
# 1. Activate virtual environment
task\Scripts\activate          # Windows
source task/bin/activate       # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python -c "import database.database as db; db.init_database()"

# 4. Populate sample data (optional)
python setup_data.py inject
python setup_data.py direct  # Add directly to database (faster)
# 5. Start server
uvicorn main:app --reload

# 6. Visit API documentation
# http://localhost:8000/docs
```

---

## Features

-  Create, read, update, and delete tasks
-  Filter tasks by status, priority, and category
-  Sort tasks by due date, creation date, or update date
-  Partial updates (PATCH) and full replacement (PUT)
-  Input validation with Pydantic
-  Automatic timestamp tracking
-  SQLite database with constraints and triggers
-  RESTful API design with proper HTTP status codes

---

## Technology Stack

- **Language:** Python 3.8+
- **Framework:** FastAPI
- **Database:** SQLite3
- **Validation:** Pydantic
- **Server:** Uvicorn

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

**1. Clone Repository**
```bash
git clone <repository-url>
cd task-management-api
```

**2. Activate Virtual Environment**

Windows:
```bash
task\Scripts\activate
```

Mac/Linux:
```bash
source task/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Initialize Database**
```bash
python -c "import database.database as db; db.init_database()"
```

**5. Start Server**
```bash
uvicorn main:app --reload
```

**6. Access API**
- Server: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Data Population

Populate the database with 25 sample tasks for testing.

### Quick Setup
```bash
# Start server first
uvicorn main:app --reload

# In another terminal, populate data
python setup_data.py inject
```

### Available Commands
```bash
python setup_data.py clear   # Clear all tasks
python setup_data.py inject  # Add 25 sample tasks
python setup_data.py direct  # Add directly to database (faster)
python setup_data.py verify  # Show statistics
python setup_data.py reset   # Complete reset
```

### Interactive Menu
```bash
python setup_data.py
```

### Sample Data Overview

- **25 tasks** across 6 categories (personal, work, learning, health, home, urgent)
- **Status:** 40% pending, 30% in_progress, 30% completed
- **Priority:** 35% high, 40% medium, 25% low
- **Due dates:** 5 days overdue to 60 days future

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Health Check

**GET /**

Check API status
```json
{
  "message": "Task Management API",
  "status": "running",
  "docs": "/docs"
}
```

---

### Tasks

#### Create Task

**POST /api/tasks**

**Request:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "status": "pending",
  "priority": "high",
  "category": "personal",
  "due_date": "2026-01-30"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, and bread",
  "status": "pending",
  "priority": "high",
  "category": "personal",
  "due_date": "2026-01-30",
  "created_at": "2026-01-26 10:30:00",
  "updated_at": "2026-01-26 10:30:00"
}
```

---

#### Get All Tasks

**GET /api/tasks**

**Query Parameters:**
- `status` - Filter by status (pending | in_progress | completed)
- `priority` - Filter by priority (low | medium | high)
- `category` - Filter by category
- `sort_by` - Sort by field (due_date | created_at | updated_at)
- `order` - Sort order (asc | desc)

**Examples:**
```bash
GET /api/tasks
GET /api/tasks?status=pending
GET /api/tasks?priority=high&sort_by=due_date&order=asc
GET /api/tasks?status=completed&category=personal
```

**Response:** `200 OK`

---

#### Get Task by ID

**GET /api/tasks/{id}**

**Response:** `200 OK` or `404 Not Found`

---

#### Update Task (Partial)

**PATCH /api/tasks/{id}**

Update only provided fields.

**Request:**
```json
{
  "status": "completed"
}
```

**Response:** `200 OK` or `404 Not Found`

---

#### Replace Task (Full)

**PUT /api/tasks/{id}**

All fields must be provided.

**Request:**
```json
{
  "title": "Updated Title",
  "description": "New description",
  "status": "in_progress",
  "priority": "medium",
  "category": "work",
  "due_date": "2026-02-15"
}
```

**Response:** `200 OK` or `404 Not Found`

---

#### Delete Task

**DELETE /api/tasks/{id}**

**Response:** `204 No Content` or `404 Not Found`

---

## Database Schema

### Tasks Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| title | TEXT | NOT NULL, MAX 200 chars | Task title |
| description | TEXT | - | Detailed description |
| status | TEXT | CHECK: pending, in_progress, completed | Task status |
| priority | TEXT | CHECK: low, medium, high | Task priority |
| category | TEXT | - | Task category |
| due_date | TEXT | - | Due date (YYYY-MM-DD) |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TEXT | AUTO-UPDATED | Last update timestamp |

### Triggers

- **updated_task** - Automatically updates `updated_at` on any UPDATE

---

## Validation Rules

### Required Fields
- `title` (max 200 characters)
- `status` (pending | in_progress | completed)
- `priority` (low | medium | high)
- `category`
- `due_date` (format: YYYY-MM-DD)

### Optional Fields
- `description`

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Testing

### Run Tests
```bash
# Start server
uvicorn main:app --reload

# Run tests with pytest
pip install pytest
pytest test.py -v
```

---

## Example Usage

### Python Requests
```python
import requests

BASE_URL = "http://localhost:8000"

# Create task
task_data = {
    "title": "Buy groceries",
    "description": "Milk and eggs",
    "status": "pending",
    "priority": "high",
    "category": "personal",
    "due_date": "2026-01-30"
}
response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
print(response.json())

# Get all tasks
response = requests.get(f"{BASE_URL}/api/tasks")
print(response.json())

# Update task
response = requests.patch(f"{BASE_URL}/api/tasks/1", 
                         json={"status": "completed"})
print(response.json())
```

---

## Project Structure
```
task-management-api/
├── main.py                 # API endpoints
├── database/
│   └── database.py        # Database operations
├── validation_models.py   # Pydantic models
├── test.py               # Test suite
├── setup_data.py     # Data population script
├── tasks_db.db           # SQLite database
├── task/                 # Virtual environment
└── README.md
```

---

## Design Decisions

### PATCH vs PUT
- **PATCH** - Partial updates (only provided fields)
- **PUT** - Full replacement (all fields required)

### Automatic Timestamps
Database trigger updates `updated_at` automatically on modifications.

### Validation
Pydantic provides automatic validation, type safety, and clear error messages.

---

## Error Handling

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "status"],
      "msg": "value is not a valid enumeration member"
    }
  ]
}
```

### Not Found (404)
```json
{
  "detail": "Task not found"
}
```

---

## Troubleshooting

### Port Already in Use
```bash
uvicorn main:app --reload --port 8001
```

### Module Not Found
```bash
# Activate virtual environment
task\Scripts\activate          # Windows
source task/bin/activate       # Mac/Linux
```

### Database Locked
Close all database connections and restart server.

### IDs Not Starting at 1
```bash
python setup_data.py clear  # Resets counters
```

---

## Requirements
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
```

Install:
```bash
pip install -r requirements.txt
```

---

## License

MIT License



## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLite](https://www.sqlite.org/)