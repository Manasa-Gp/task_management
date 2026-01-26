"""
pytest test suite for Task Management API
Run with: pytest test_api_pytest.py -v
"""

import pytest
import requests
import json

BASE_URL = 'http://localhost:8000'


# ========================================
# Fixtures (Reusable Setup)
# ========================================

@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        "title": "Buy groceries",
        "description": "Milk, eggs, and bread",
        "status": "pending",
        "priority": "high",
        "category": "personal",
        "due_date": "2026-01-25"
    }


@pytest.fixture
def created_task(sample_task_data):
    """Create a task and return it (with cleanup)"""
    response = requests.post(f"{BASE_URL}/api/tasks", json=sample_task_data)
    task = response.json()
    
    yield task  # Provide to test
    
    # Cleanup: Delete task after test
    try:
        requests.delete(f"{BASE_URL}/api/tasks/{task['id']}")
    except:
        pass


# ========================================
# POST Tests (Create)
# ========================================

def test_create_task(sample_task_data):
    """Test creating a new task"""
    response = requests.post(f"{BASE_URL}/api/tasks", json=sample_task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == sample_task_data["title"]
    assert data["status"] == sample_task_data["status"]
    assert data["priority"] == sample_task_data["priority"]
    
    # Cleanup
    requests.delete(f"{BASE_URL}/api/tasks/{data['id']}")


def test_create_task_completed_status():
    """Test creating a task with completed status"""
    task_data = {
        "title": "Completed Task",
        "description": "Already done",
        "status": "completed",
        "priority": "high",
        "category": "personal",
        "due_date": "2026-01-27"
    }
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "completed"
    
    # Cleanup
    requests.delete(f"{BASE_URL}/api/tasks/{data['id']}")


def test_create_task_missing_title():
    """Test creating task without required title"""
    task_data = {
        "description": "Missing title",
        "status": "pending",
        "priority": "low",
        "category": "test",
        "due_date": "2026-02-01"
    }
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    
    assert response.status_code == 422  # Validation error


def test_create_task_invalid_status():
    """Test creating task with invalid status"""
    task_data = {
        "title": "Invalid Status",
        "description": "Test",
        "status": "invalid_status",
        "priority": "low",
        "category": "test",
        "due_date": "2026-02-01"
    }
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    
    assert response.status_code == 422  # Validation error


# ========================================
# GET Tests (Read)
# ========================================



def test_get_all_tasks():
    """Test getting all tasks"""
    response = requests.get(f"{BASE_URL}/api/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_task_by_id(created_task):
    """Test getting a specific task by ID"""
    task_id = created_task["id"]
    response = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == created_task["title"]


def test_get_task_not_found():
    """Test getting non-existent task returns 404"""
    response = requests.get(f"{BASE_URL}/api/tasks/99999")
    
    assert response.status_code == 404


# ========================================
# GET with Query Parameters
# ========================================

def test_get_tasks_filter_by_status():
    """Test filtering tasks by status"""
    # Create a task with specific status
    task_data = {
        "title": "Test Filter",
        "description": "Test",
        "status": "completed",
        "priority": "low",
        "category": "test",
        "due_date": "2026-02-01"
    }
    create_response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    created_id = create_response.json()["id"]
    
    # Test filter
    response = requests.get(f"{BASE_URL}/api/tasks?status=completed")
    
    assert response.status_code == 200
    tasks = response.json()
    
    # All returned tasks should have status 'completed'
    for task in tasks:
        assert task["status"] == "completed"
    
    # Cleanup
    requests.delete(f"{BASE_URL}/api/tasks/{created_id}")


def test_get_tasks_filter_by_priority():
    """Test filtering tasks by priority"""
    response = requests.get(f"{BASE_URL}/api/tasks?priority=high")
    
    assert response.status_code == 200
    tasks = response.json()
    
    for task in tasks:
        assert task["priority"] == "high"


def test_get_tasks_filter_by_category():
    """Test filtering tasks by category"""
    response = requests.get(f"{BASE_URL}/api/tasks?category=personal")
    
    assert response.status_code == 200
    tasks = response.json()
    
    for task in tasks:
        assert task["category"] == "personal"


def test_get_tasks_sort_by_due_date():
    """Test sorting tasks by due_date"""
    response = requests.get(f"{BASE_URL}/api/tasks?sort_by=due_date&order=asc")
    
    assert response.status_code == 200
    tasks = response.json()
    
    # Verify ascending order
    if len(tasks) > 1:
        for i in range(len(tasks) - 1):
            assert tasks[i]["due_date"] <= tasks[i + 1]["due_date"]


def test_get_tasks_combined_filters():
    """Test combining multiple filters"""
    response = requests.get(f"{BASE_URL}/api/tasks?status=pending&priority=high")
    
    assert response.status_code == 200
    tasks = response.json()
    
    for task in tasks:
        assert task["status"] == "pending"
        assert task["priority"] == "high"


# ========================================
# PATCH Tests (Partial Update)
# ========================================

def test_patch_task(created_task):
    """Test updating task with PATCH (partial update)"""
    task_id = created_task["id"]
    update_data = {"title": "Updated Title"}
    
    response = requests.patch(f"{BASE_URL}/api/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    # Other fields should remain unchanged
    assert data["status"] == created_task["status"]
    assert data["priority"] == created_task["priority"]


def test_patch_task_status(created_task):
    """Test updating only task status"""
    task_id = created_task["id"]
    update_data = {"status": "completed"}
    
    response = requests.patch(f"{BASE_URL}/api/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["title"] == created_task["title"]  # Unchanged


def test_patch_task_not_found():
    """Test patching non-existent task"""
    update_data = {"title": "New Title"}
    response = requests.patch(f"{BASE_URL}/api/tasks/99999", json=update_data)
    
    assert response.status_code == 404


# ========================================
# PUT Tests (Full Replacement) - If you have PUT endpoint
# ========================================

def test_put_task(created_task):
    """Test full replacement with PUT"""
    task_id = created_task["id"]
    update_data = {
        "title": "Completely New Task",
        "description": "New description",
        "status": "in_progress",
        "priority": "low",
        "category": "work",
        "due_date": "2026-02-15"
    }
    
    response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]
    assert data["priority"] == update_data["priority"]


# ========================================
# DELETE Tests
# ========================================



def test_delete_task():
    """Test deleting a task"""
    # Create a task to delete
    task_data = {
        "title": "Delete Me",
        "description": "Test",
        "status": "pending",
        "priority": "low",
        "category": "test",
        "due_date": "2026-02-01"
    }
    create_response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Delete it
    response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test deleting non-existent task"""
    response = requests.delete(f"{BASE_URL}/api/tasks/99999")
    
    assert response.status_code == 404


# ========================================
# Parametrized Tests
# ========================================

@pytest.mark.parametrize("status", ["pending", "in_progress", "completed"])
def test_create_task_all_statuses(status):
    """Test creating tasks with different statuses"""
    task_data = {
        "title": f"Task with {status} status",
        "description": "Test",
        "status": status,
        "priority": "medium",
        "category": "test",
        "due_date": "2026-02-01"
    }
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    
    assert response.status_code == 201
    assert response.json()["status"] == status
    
    # Cleanup
    requests.delete(f"{BASE_URL}/api/tasks/{response.json()['id']}")


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_create_task_all_priorities(priority):
    """Test creating tasks with different priorities"""
    task_data = {
        "title": f"Task with {priority} priority",
        "description": "Test",
        "status": "pending",
        "priority": priority,
        "category": "test",
        "due_date": "2026-02-01"
    }
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    
    assert response.status_code == 201
    assert response.json()["priority"] == priority
    
    # Cleanup
    requests.delete(f"{BASE_URL}/api/tasks/{response.json()['id']}")



