# test_put_detailed.py
import requests
import json

BASE_URL = "http://localhost:8000"

# First, create a task to update
create_response = requests.post(
    f"{BASE_URL}/api/tasks",
    json={
        "title": "Original Title",
        "description": "Original description",
        "status": "pending",
        "priority": "low",
        "category": "test",
        "due_date": "2026-01-30"
    }
)

print("CREATE RESPONSE:")
print(json.dumps(create_response.json(), indent=2))
task_id = create_response.json()["id"]
print(f"\nCreated task ID: {task_id}")

# Now update it
print("\n" + "=" * 50)
print("UPDATING TASK...")
print("=" * 50)

update_response = requests.put(
    f"{BASE_URL}/api/tasks/{task_id}",
    json={
        "title": "UPDATED TITLE"
    }
)

print(f"Status: {update_response.status_code}")
print(f"Response: {json.dumps(update_response.json(), indent=2)}")