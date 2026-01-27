# Task Management REST API

A RESTful API for managing tasks with full CRUD operations, filtering, sorting, and validation. Built with FastAPI and SQLite.

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

- **Language:** Python 3.x
- **Framework:** FastAPI
- **Database:** SQLite3
- **Validation:** Pydantic
- **Server:** Uvicorn

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd task-management-api
```

### 2. Navigate to Virtual Environment
```bash
cd <Project-Folder>\task
```

### 3. Activate Virtual Environment

**Windows:**
```bash
task\Scripts\activate
```

**Mac/Linux:**
```bash
source task/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize Database
```bash
python -c "import database.database as db; db.init_database()"
```

### 6. Run the Server
```bash
uvicorn main:app --reload
```

Server will start at: **http://localhost:8000**

### 7. View API Documentation

Open your browser and navigate to:
- Swagger UI: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Health Check

#### `GET /`
Check API status

**Response:**
```json
{
  "message": "Task Management API",
  "status": "running",
  "docs": "/docs"
}
```

---

### Tasks

#### `POST /api/tasks`
Create a new task

**Request Body:**
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

#### `GET /api/tasks`
Get all tasks with optional filters and sorting

**Query Parameters:**
- `status` - Filter by status (pending | in_progress | completed)
- `priority` - Filter by priority (low | medium | high)
- `category` - Filter by category (string)
- `sort_by` - Sort by field (due_date | created_at | updated_at)
- `order` - Sort order (asc | desc)

**Examples:**
```bash
# Get all tasks
GET /api/tasks

# Get pending tasks
GET /api/tasks?status=pending

# Get high priority tasks sorted by due date
GET /api/tasks?priority=high&sort_by=due_date&order=asc

# Get completed personal tasks
GET /api/tasks?status=completed&category=personal
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "status": "pending",
    ...
  },
  {
    "id": 2,
    "title": "Finish report",
    "status": "in_progress",
    ...
  }
]
```

---

#### `GET /api/tasks/{id}`
Get a specific task by ID

**Example:**
```bash
GET /api/tasks/1
```

**Response:** `200 OK` or `404 Not Found`

---

#### `PATCH /api/tasks/{id}`
Partially update a task (only provided fields are updated)

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response:** `200 OK` or `404 Not Found`

---

#### `PUT /api/tasks/{id}`
Fully replace a task (all fields must be provided)

**Request Body:**
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

#### `DELETE /api/tasks/{id}`
Delete a task

**Example:**
```bash
DELETE /api/tasks/1
```

**Response:** `204 No Content` or `404 Not Found`

---

## Database Schema

### Tasks Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique task identifier |
| title | TEXT | NOT NULL, MAX 200 chars | Task title |
| description | TEXT | - | Detailed description (optional) |
| status | TEXT | CHECK: pending, in_progress, completed | Task status |
| priority | TEXT | CHECK: low, medium, high | Task priority |
| category | TEXT | - | Task category |
| due_date | TEXT | - | Due date (YYYY-MM-DD format) |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TEXT | AUTO-UPDATED | Last update timestamp |

### Database Triggers

- **updated_task**: Automatically updates `updated_at` timestamp on any UPDATE operation

---

## Validation Rules

### Required Fields
- `title` (max 200 characters)
- `status` (must be: pending, in_progress, or completed)
- `priority` (must be: low, medium, or high)
- `category`
- `due_date` (format: YYYY-MM-DD)

### Optional Fields
- `description`

### Date Format
- Due date must match: `YYYY-MM-DD` (e.g., 2026-01-30)

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request data |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Project Structure
```
task-management-api/
├── main.py                 # API endpoints and routes
├── database/
│   └── database.py        # Database operations and queries
├── validation_models.py   # Pydantic validation models
├── test.py               # Test suite
├── tasks_db.db           # SQLite database (generated)
├── task/                 # Virtual environment
└── README.md
```

---


## Testing

### Run Tests
```bash
# Make sure server is running first
uvicorn main:app --reload
```

### Run with pytest 
```bash
pip install pytest
pytest test.py -v
```

---

## Example Usage


### Using Python Requests
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

## Design Decisions

### PATCH vs PUT
- **PATCH** (`/api/tasks/{id}`): Partial updates - only update fields provided
- **PUT** (`/api/tasks/{id}`): Full replacement - all fields must be provided

This provides flexibility: use PATCH for quick status updates, use PUT for complete task replacement.

### Automatic Timestamps
Database trigger automatically updates `updated_at` on any modification, ensuring accurate tracking without manual intervention.

### Validation Strategy
Pydantic models provide:
- Automatic validation before database operations
- Type safety
- Clear error messages (422 responses)
- Auto-generated API documentation

### Query Parameters
All filters are optional and can be combined for powerful querying:
```
/api/tasks?status=pending&priority=high&sort_by=due_date&order=asc
```

---

## Error Handling

### Validation Errors (422)
```json
{
  "detail": [
    {
      "loc": ["body", "status"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
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

### Server Error (500)
```json
{
  "detail": "Failed to create task"
}
```

---

## Requirements

Create `requirements.txt`:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Future Enhancements

-  Pagination for large result sets
-  Search functionality (by title/description)
-  Statistics endpoint (total, completed, pending counts)
-  User authentication and authorization
-  Task tags/labels
-  Due date reminders
-  Task history/audit log
-  Export to CSV/JSON

---

## Troubleshooting

### Port Already in Use
```bash
# Change port
uvicorn main:app --reload --port 8001
```

### Database Locked Error
```bash
# Close all database connections and restart server
```

### Module Not Found
```bash
# Make sure virtual environment is activated
source task/bin/activate  # Mac/Linux
task\Scripts\activate     # Windows
```

---

## License

MIT License

---

## Author

[Your Name]

---

## Contact

For questions or issues, please contact [your-email@example.com]

---

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Validation with [Pydantic](https://docs.pydantic.dev/)
- Database: [SQLite](https://www.sqlite.org/)