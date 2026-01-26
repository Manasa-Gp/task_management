from fastapi import FastAPI,HTTPException
from typing import Optional
import validation_models as vm
import database.database as db



app = FastAPI()


@app.get("/")
def root():
    """
    Root endpoint - API health check

    Returns:
        dict: API status information and documentation link
    """
    return {
        "message": "Task Management API",
        "status": "running",
        "docs": "/docs"
    }

@app.post("/api/tasks",status_code=201)
def create_task(task:vm.TaskCreate):
    """
    Create a new task

    Args:
        task (TaskCreate): Task data including title, description, status, 
                        priority, category, and due_date

    Returns:
        dict: Created task object with generated ID and timestamps

    Raises:
        HTTPException: 500 if task creation fails
        HTTPException: 422 if validation fails (automatic from Pydantic)

    Example:
        POST /api/tasks
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
            "priority": "high",
            "category": "personal",
            "due_date": "2026-01-30"
        }
    """
    title =  task.title
    description =  task.description
    status =   task.status.value
    priority =  task.priority.value
    category =  task.category
    due_date =  task.due_date
    
    task_object = db.create_task_db(title,description,status,priority,category,due_date)

    if not task_object:
        raise HTTPException(
    status_code=500,  
    detail="Failed to create task"
)


    return task_object



@app.get("/api/tasks")
def get_all_tasks(
    status: Optional[vm.TaskStatus]=None,
    priority: Optional[vm.TaskPriority]=None,
    category: Optional[str]=None,
    sort_by: Optional[vm.SortByField] = None,
    order: Optional[vm.SortOrder] = vm.SortOrder.asc
    ):
    """
    Get all tasks with optional filtering and sorting

    Query Parameters:
        status (TaskStatus, optional): Filter by status (pending, in_progress, completed)
        priority (TaskPriority, optional): Filter by priority (low, medium, high)
        category (str, optional): Filter by category string
        sort_by (SortByField, optional): Sort by field (due_date, created_at, updated_at)
        order (SortOrder, optional): Sort order (asc, desc). Default: asc

    Returns:
        list: Array of task objects matching the filters. Empty array if no matches.

    Example:
        GET /api/tasks?status=pending&priority=high&sort_by=due_date&order=asc
    """

    status_str = status.value if status else None
    priority_str = priority.value if priority else None
    sort_by_str = sort_by.value if sort_by else None
    order_str = order.value if order else None
    task_list = db.get_all_tasks_db(status_str,priority_str,category,sort_by_str,order_str)
    return task_list

@app.get("/api/tasks/{task_id}")
def get_task_by_id(task_id:int):
    """
    Get a specific task by ID

    Args:
        task_id (int): Unique task identifier

    Returns:
        dict: Task object with all fields

    Raises:
        HTTPException: 404 if task not found

    Example:
        GET /api/tasks/5
    """
    task= db.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404,detail="task not found")
    return task


# if you dont return the response in api it wont be reflected in test    
@app.put("/api/tasks/{task_id}")
def update_task_by_id(task_id:int,task:vm.TaskCreate):
    """
    Fully replace a task (all fields must be provided)

    This endpoint replaces the entire task resource. All fields
    must be provided in the request body. Use PATCH for partial updates.

    Args:
        task_id (int): Unique task identifier
        task (TaskCreate): Complete task data (all fields required except description)

    Returns:
        dict: Updated task object with new updated_at timestamp

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 422 if validation fails or missing required fields

    Example:
        PUT /api/tasks/5
        {
            "title": "Updated Title",
            "description": "New description",
            "status": "in_progress",
            "priority": "medium",
            "category": "work",
            "due_date": "2026-02-15"
        }
    """
    data = task.model_dump(exclude_none=True)
    task = db.update_task_by_id_db(task_id,data)
    if not task:
        raise HTTPException(status_code = 404, detail= "task not found")
    return task

@app.patch("/api/tasks/{task_id}")
def patch_task_by_id(task_id: int, task: vm.TaskUpdate):
    """
    Partially update a task (only provided fields are updated)

    This endpoint updates only the fields provided in the request body.
    All other fields remain unchanged. The updated_at timestamp is
    automatically updated by the database trigger.

    Args:
        task_id (int): Unique task identifier
        task (TaskUpdate): Task fields to update (all fields optional)

    Returns:
        dict: Updated task object with new updated_at timestamp

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 422 if validation fails

    Example:
        PATCH /api/tasks/5
        {
            "status": "completed"
        }
    """
    data = task.model_dump(exclude_none=True)
    updated_task = db.patch_task_by_id_db(task_id, data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/api/tasks/{task_id}",status_code=204)
def delete_task_by_id(task_id:int):
    """
    Delete a task by ID

    Args:
        task_id (int): Unique task identifier

    Returns:
        None: 204 No Content on successful deletion

    Raises:
        HTTPException: 404 if task not found

    Example:
        DELETE /api/tasks/5
    """
    if not db.delete_task_by_id(task_id):
        raise HTTPException(status_code = 404, detail= "task not found")
        

