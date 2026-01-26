from pydantic import BaseModel,Field
from enum import Enum
from typing import Optional


class SortByField(str,Enum):
    """
    Enum for valid sort field options

    Values:
        due_date: Sort by task due date
        created_at: Sort by creation timestamp
        updated_at: Sort by last update timestamp
    """
    due_date = "due_date"
    created_at = "created_at"
    updated_at="updated_at"

class SortOrder(str,Enum):
    """
    Enum for sort order direction

    Values:
        asc: Ascending order (A-Z, 0-9, oldest-newest)
        desc: Descending order (Z-A, 9-0, newest-oldest)
    """
    asc ="asc"
    desc = "desc"

class TaskStatus(str,Enum):
    """
    Enum for valid task status values

    Values:
        pending: Task not yet started
        in_progress: Task currently being worked on
        completed: Task finished
    """
    pending = "pending"
    in_progress= "in_progress"
    completed= "completed"

class TaskPriority(str,Enum):
    """
    Enum for valid task priority levels

    Values:
        low: Low priority task
        medium: Medium priority task
        high: High priority task
    """
    low = "low"
    medium = "medium"
    high = "high"

class TaskCreate(BaseModel):
    """
    Pydantic model for creating new tasks (POST requests)

    Used for task creation and full replacement (PUT). Validates all
    required fields and formats. Description is optional, all other
    fields are required.

    Attributes:
        title (str): Task title, max 200 characters
        description (Optional[str]): Detailed description, optional
        status (TaskStatus): Must be pending, in_progress, or completed
        priority (TaskPriority): Must be low, medium, or high
        category (str): Task category (any string)
        due_date (str): ISO 8601 date format (YYYY-MM-DD)

    Validation:
        - Title length <= 200 characters
        - Due date matches regex: ^\d{4}-\d{2}-\d{2}$
        - Status must be valid enum value
        - Priority must be valid enum value

    Example:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
            "priority": "high",
            "category": "personal",
            "due_date": "2026-01-30"
        }
    """
    
    title: str = Field(max_length = 200)
    description: Optional[str] = None 
    status: TaskStatus
    priority: TaskPriority
    category: str
    due_date: str = Field(pattern = r'^\d{4}-\d{2}-\d{2}$')

class TaskUpdate(BaseModel):
    """
    Pydantic model for partial task updates (PATCH requests)

    All fields are optional, allowing partial updates. Only fields
    provided in the request will be updated. Used with exclude_none=True
    to filter out unset fields.

    Attributes:
        title (Optional[str]): Task title, max 200 characters
        description (Optional[str]): Detailed description
        status (Optional[TaskStatus]): Task status
        priority (Optional[TaskPriority]): Task priority
        category (Optional[str]): Task category
        due_date (Optional[str]): Due date in YYYY-MM-DD format

    Validation:
        - If title provided: length <= 200 characters
        - If due_date provided: matches regex ^\d{4}-\d{2}-\d{2}$
        - If status provided: must be valid enum value
        - If priority provided: must be valid enum value

    Example:
        {
            "status": "completed"
        }
        
        {
            "title": "Updated Title",
            "priority": "low"
        }
    """
    title:Optional[str] = None
    description: Optional[str] = None 
    status: Optional[TaskStatus]=None
    priority: Optional[TaskPriority] = None
    category: Optional[str] =None
    due_date: Optional[str] = Field(default=None,pattern = r'^\d{4}-\d{2}-\d{2}$')


