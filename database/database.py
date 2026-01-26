import sqlite3


def get_connection():
    """
    Create and return a SQLite database connection

    Returns:
        sqlite3.Connection: Active database connection to tasks_db.db

    Note:
        Connection must be closed after use
    """
    connection = sqlite3.connect("tasks_db.db")
    return connection 


def init_database():
    """
    Initialize the database schema

    Creates the TASKS table with all required fields, constraints, and triggers
    if they don't already exist. Safe to call multiple times (idempotent).

    Table Structure:
        - id: INTEGER PRIMARY KEY AUTOINCREMENT
        - title: TEXT NOT NULL (max 200 chars)
        - description: TEXT (optional)
        - status: TEXT CHECK (pending | in_progress | completed)
        - priority: TEXT CHECK (low | medium | high)
        - category: TEXT
        - due_date: TEXT (ISO 8601 format YYYY-MM-DD)
        - created_at: TEXT (auto-generated timestamp)
        - updated_at: TEXT (auto-updated via trigger)

    Triggers:
        - updated_task: Automatically updates updated_at on any UPDATE operation

    Raises:
        Prints error message if database operation fails

    Example:
        init_database()  # Safe to call on startup
    """
        
    connection = get_connection()
    cursor = connection.cursor()

    statement_1 = """
    CREATE TABLE IF NOT EXISTS TASKS
    (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TITLE TEXT NOT NULL CHECK (LENGTH(TITLE)<=200),
    DESCRIPTION TEXT,
    STATUS TEXT CHECK (STATUS IN ('pending','in_progress','completed')),
    PRIORITY TEXT CHECK (PRIORITY IN ('low','medium','high')),
    CATEGORY TEXT,
    due_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT 
    )
    """
    statement_2 = """
    CREATE TRIGGER IF NOT EXISTS updated_task
    AFTER UPDATE ON TASKS
    BEGIN
        UPDATE TASKS SET updated_at = CURRENT_TIMESTAMP WHERE id = New.id;
    END;
    """
    try:
        cursor.execute(statement_1)

        cursor.execute(statement_2)

        connection.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()


def create_task_db(title,description,status,priority,category,due_date):
    """
    Create a new task in the database

    Args:
        title (str): Task title (required, max 200 chars)
        description (str): Detailed description (optional)
        status (str): Task status (pending, in_progress, completed)
        priority (str): Task priority (low, medium, high)
        category (str): Task category
        due_date (str): Due date in YYYY-MM-DD format

    Returns:
        dict: Created task object with all 9 fields including:
            - id (generated)
            - created_at (auto-generated)
            - updated_at (auto-generated)
        None: If creation fails

    Example:
        task = create_task_db(
            "Buy groceries",
            "Milk and eggs",
            "pending",
            "high",
            "personal",
            "2026-01-30"
        )
    """
    connection = get_connection()
    cursor = connection.cursor()

    statement_1 = """
    INSERT INTO TASKS (title,description,status,priority,category,due_date,updated_at)
     VALUES (?,?,?,?,?,?,CURRENT_TIMESTAMP)
    """
    try:
        cursor.execute(statement_1,(title,description,status,priority,category,due_date))

        connection.commit()
        

        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM TASKS WHERE id = ?",(task_id,))
        row = cursor.fetchone()

        if not row:
            return None
        
        task = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "category": row[5],
            "due_date": row[6],
            "created_at": row[7],
            "updated_at": row[8]
        }
        return task



    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    
    finally:
        connection.close()

def get_all_tasks_db(status=None,priority=None,category=None,sort_by=None,order="asc"):
    """
    Get all tasks with optional filtering and sorting

    Builds dynamic SQL query based on provided filters. All parameters
    are optional - calling without arguments returns all tasks.

    Args:
        status (str, optional): Filter by status value
        priority (str, optional): Filter by priority value
        category (str, optional): Filter by category string
        sort_by (str, optional): Column to sort by (due_date, created_at, updated_at)
        order (str, optional): Sort direction (asc, desc). Default: asc

    Returns:
        list: Array of task dictionaries with all fields
        Empty list: If no tasks match filters or table is empty

    Note:
        Uses parameterized queries to prevent SQL injection

    Example:
        tasks = get_all_tasks_db(status="pending", priority="high", 
                                sort_by="due_date", order="asc")
    """
    connection = get_connection()
    cursor = connection.cursor()

    statement = """
       SELECT * FROM TASKS where 1 = 1
     """
    params = []
    if status:
        statement += " AND status = ?"
        params.append(status)
    if priority:
        statement += " AND priority = ?"
        params.append(priority)
    if category:
        statement += " AND category = ?"
        params.append(category)
    if sort_by:
        statement += f" ORDER BY {sort_by} {order}"
    
    try:
        cursor.execute(statement, params)
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            task = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "category": row[5],
            "due_date": row[6],
            "created_at": row[7],
            "updated_at": row[8]
             }
            tasks.append(task)
        return tasks
    
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        connection.close()


def get_task_by_id(task_id):
    """
    Get a specific task by ID

    Args:
        task_id (int): Unique task identifier

    Returns:
        dict: Task object with all 9 fields
        None: If task not found

    Example:
        task = get_task_by_id(5)
        if task:
            print(task['title'])
    """
        
    connection = get_connection()
    cursor = connection.cursor()

    statement ="""
    SELECT * FROM TASKS WHERE id = ?
    """
    try:
        cursor.execute(statement,(task_id,))
        row = cursor.fetchone()
        if not row:
            return None
        task = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "category": row[5],
            "due_date": row[6],
            "created_at": row[7],
            "updated_at": row[8]
        }
        return task
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        connection.close()
        
def patch_task_by_id_db(task_id, data):
    """
    Partially update a task (only provided fields)

    Dynamically builds UPDATE query including only fields present in the
    data dictionary. Fields not in data remain unchanged. The database
    trigger automatically updates the updated_at timestamp.

    Args:
        task_id (int): Unique task identifier
        data (dict): Dictionary containing only fields to update
                    Keys: title, description, status, priority, category, due_date

    Returns:
        dict: Updated task object with all fields including new updated_at
        None: If task not found or update fails

    Example:
        updated = patch_task_by_id_db(5, {"status": "completed"})
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    set_parts = []
    params = []

    
    for field in ["title", "description", "status", "priority", "category", "due_date"]:
        if field in data and data[field] is not None:
            set_parts.append(f"{field} = ?")
            params.append(data[field])

    try:
        
        # Build and execute UPDATE
        statement = f"UPDATE TASKS SET {', '.join(set_parts)} WHERE id = ?"
        params.append(task_id)
        
        cursor.execute(statement, params)
        connection.commit()
        
        # Fetch updated task
        cursor.execute("SELECT * FROM TASKS WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        # Convert to dictionary
        task = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "category": row[5],
            "due_date": row[6],
            "created_at": row[7],
            "updated_at": row[8]
        }
        
        return task
        
    except sqlite3.Error as e:
        return None
        
    finally:
        connection.close()

def update_task_by_id_db(task_id, data):
    """
    Fully replace a task (all fields updated)

    Updates all task fields with new values. Intended for PUT operations
    where all fields are provided. The database trigger automatically
    updates the updated_at timestamp.

    Args:
        task_id (int): Unique task identifier
        data (dict): Dictionary containing all task fields
                    Keys: title, description, status, priority, category, due_date

    Returns:
        dict: Updated task object with all fields including new updated_at
        None: If task not found or update fails

    Example:
        updated = update_task_by_id_db(5, {
            "title": "New Title",
            "description": "New desc",
            "status": "completed",
            "priority": "low",
            "category": "work",
            "due_date": "2026-02-15"
        })
    """
    connection = get_connection()
    cursor = connection.cursor()
    field_list = ["title", "description", "status", "priority", "category", "due_date"]
    set_updates = []
    params = []
    for field in field_list:
        set_updates.append(f"{field} = ?")
        params.append(data.get(field,None))

    try:
        # Build and execute UPDATE
        statement = f"UPDATE TASKS SET {', '.join(set_updates)} WHERE id = ?"
        params.append(task_id)
        
        cursor.execute(statement, params)
        connection.commit()
        
        # Fetch updated task
        cursor.execute("SELECT * FROM TASKS WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        # Convert to dictionary
        task = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "category": row[5],
            "due_date": row[6],
            "created_at": row[7],
            "updated_at": row[8]
        }
        
        return task
        
    except sqlite3.Error as e:
        return None
        
    finally:
        connection.close()


def delete_task_by_id(task_id):
    """
    Delete a task from the database

    Checks if task exists before attempting deletion to provide
    accurate 404 responses.

    Args:
        task_id (int): Unique task identifier

    Returns:
        bool: True if task was deleted successfully
        bool: False if task not found

    Example:
        if delete_task_by_id(5):
            print("Task deleted")
        else:
            print("Task not found")
    """
    connection =get_connection()
    cursor = connection.cursor()
    statement = """
    DELETE FROM TASKS WHERE id = ?
    """
    try:
        cursor.execute("SELECT * FROM TASKS WHERE id = ?",(task_id,))
        row = cursor.fetchone()
        if not row:
            return False
        cursor.execute(statement,(task_id,))
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        connection.close()

   