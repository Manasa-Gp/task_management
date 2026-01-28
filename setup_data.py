"""
Data Population Script for Task Management API (Assignment 1)
Run this to populate the tasks database with sample data
"""

import sqlite3
import requests
from datetime import datetime, timedelta

DB_FILE = 'tasks_db.db'
BASE_URL = "http://localhost:8000"


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_FILE)


def clear_all_tasks():
    """Clear all tasks from database"""
    connection = get_connection()
    cursor = connection.cursor()
    
    print("\n" + "=" * 60)
    print("CLEARING ALL TASKS")
    print("=" * 60)
    
    try:
        cursor.execute("DELETE FROM TASKS")
        count = cursor.rowcount
        
        # Reset AUTOINCREMENT
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='TASKS'")
        
        connection.commit()
        
        print(f"✅ Deleted {count} tasks")
        print(f"✅ Reset ID counter")
        print("=" * 60 + "\n")
        
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    finally:
        connection.close()


def verify_tasks():
    """Verify task counts"""
    connection = get_connection()
    cursor = connection.cursor()
    
    print("\n" + "=" * 60)
    print("TASK VERIFICATION")
    print("=" * 60 + "\n")
    
    try:
        # Total tasks
        cursor.execute("SELECT COUNT(*) FROM TASKS")
        total = cursor.fetchone()[0]
        
        # By status
        cursor.execute("SELECT status, COUNT(*) FROM TASKS GROUP BY status")
        status_counts = cursor.fetchall()
        
        # By priority
        cursor.execute("SELECT priority, COUNT(*) FROM TASKS GROUP BY priority")
        priority_counts = cursor.fetchall()
        
        print(f"📊 Total Tasks: {total}")
        print(f"\n📌 By Status:")
        for status, count in status_counts:
            print(f"   {status:15} {count:3}")
        
        print(f"\n⚡ By Priority:")
        for priority, count in priority_counts:
            print(f"   {priority:15} {count:3}")
        
        print("\n" + "=" * 60 + "\n")
        
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    finally:
        connection.close()


def show_sample_tasks():
    """Show sample tasks"""
    connection = get_connection()
    cursor = connection.cursor()
    
    print("\n" + "=" * 60)
    print("SAMPLE TASKS")
    print("=" * 60 + "\n")
    
    try:
        cursor.execute("SELECT id, title, status, priority, due_date FROM TASKS LIMIT 10")
        tasks = cursor.fetchall()
        
        for task in tasks:
            print(f"ID {task[0]:2} - {task[1]:40} | {task[2]:12} | {task[3]:6} | Due: {task[4]}")
        
        print("\n" + "=" * 60 + "\n")
        
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    finally:
        connection.close()


# ============================================================
# SAMPLE TASK DATA
# ============================================================

def get_sample_tasks():
    """Generate sample task data"""
    
    today = datetime.now()
    
    tasks = [
        # Personal tasks
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, fruits, vegetables",
            "status": "pending",
            "priority": "high",
            "category": "personal",
            "due_date": (today + timedelta(days=1)).strftime('%Y-%m-%d')
        },
        {
            "title": "Schedule dentist appointment",
            "description": "Call dental clinic for cleaning appointment",
            "status": "pending",
            "priority": "medium",
            "category": "personal",
            "due_date": (today + timedelta(days=3)).strftime('%Y-%m-%d')
        },
        {
            "title": "Plan weekend trip",
            "description": "Research destinations and book accommodations",
            "status": "in_progress",
            "priority": "low",
            "category": "personal",
            "due_date": (today + timedelta(days=7)).strftime('%Y-%m-%d')
        },
        {
            "title": "Renew gym membership",
            "description": "Membership expires end of month",
            "status": "pending",
            "priority": "medium",
            "category": "personal",
            "due_date": (today + timedelta(days=10)).strftime('%Y-%m-%d')
        },
        {
            "title": "Clean garage",
            "description": "Organize tools and donate unused items",
            "status": "completed",
            "priority": "low",
            "category": "personal",
            "due_date": (today - timedelta(days=2)).strftime('%Y-%m-%d')
        },
        
        # Work tasks
        {
            "title": "Complete project proposal",
            "description": "Draft proposal for Q2 project including budget and timeline",
            "status": "in_progress",
            "priority": "high",
            "category": "work",
            "due_date": (today + timedelta(days=2)).strftime('%Y-%m-%d')
        },
        {
            "title": "Review team code submissions",
            "description": "Review and approve pull requests from team members",
            "status": "pending",
            "priority": "high",
            "category": "work",
            "due_date": (today).strftime('%Y-%m-%d')
        },
        {
            "title": "Prepare presentation slides",
            "description": "Create slides for Friday's client meeting",
            "status": "in_progress",
            "priority": "high",
            "category": "work",
            "due_date": (today + timedelta(days=3)).strftime('%Y-%m-%d')
        },
        {
            "title": "Update project documentation",
            "description": "Document new API endpoints and usage examples",
            "status": "pending",
            "priority": "medium",
            "category": "work",
            "due_date": (today + timedelta(days=5)).strftime('%Y-%m-%d')
        },
        {
            "title": "Attend team standup",
            "description": "Daily standup meeting at 9 AM",
            "status": "completed",
            "priority": "high",
            "category": "work",
            "due_date": today.strftime('%Y-%m-%d')
        },
        {
            "title": "Schedule one-on-one meetings",
            "description": "Set up meetings with direct reports",
            "status": "pending",
            "priority": "medium",
            "category": "work",
            "due_date": (today + timedelta(days=4)).strftime('%Y-%m-%d')
        },
        {
            "title": "Fix bug in production",
            "description": "Address critical bug reported by customer",
            "status": "in_progress",
            "priority": "high",
            "category": "urgent",
            "due_date": today.strftime('%Y-%m-%d')
        },
        
        # Learning tasks
        {
            "title": "Complete Python course module 3",
            "description": "Finish advanced functions and decorators section",
            "status": "in_progress",
            "priority": "medium",
            "category": "learning",
            "due_date": (today + timedelta(days=6)).strftime('%Y-%m-%d')
        },
        {
            "title": "Read documentation on FastAPI",
            "description": "Study async features and dependency injection",
            "status": "pending",
            "priority": "low",
            "category": "learning",
            "due_date": (today + timedelta(days=8)).strftime('%Y-%m-%d')
        },
        {
            "title": "Practice SQL queries",
            "description": "Complete SQL practice problems on LeetCode",
            "status": "pending",
            "priority": "medium",
            "category": "learning",
            "due_date": (today + timedelta(days=5)).strftime('%Y-%m-%d')
        },
        
        # Health tasks
        {
            "title": "Morning workout",
            "description": "30-minute cardio and strength training",
            "status": "completed",
            "priority": "high",
            "category": "health",
            "due_date": today.strftime('%Y-%m-%d')
        },
        {
            "title": "Meal prep for the week",
            "description": "Prepare healthy meals for Monday through Friday",
            "status": "pending",
            "priority": "medium",
            "category": "health",
            "due_date": (today + timedelta(days=1)).strftime('%Y-%m-%d')
        },
        {
            "title": "Track daily water intake",
            "description": "Drink at least 8 glasses of water",
            "status": "in_progress",
            "priority": "medium",
            "category": "health",
            "due_date": today.strftime('%Y-%m-%d')
        },
        
        # Home tasks
        {
            "title": "Pay utility bills",
            "description": "Pay electricity, water, and internet bills",
            "status": "pending",
            "priority": "high",
            "category": "home",
            "due_date": (today + timedelta(days=2)).strftime('%Y-%m-%d')
        },
        {
            "title": "Call plumber",
            "description": "Fix leaking kitchen faucet",
            "status": "pending",
            "priority": "high",
            "category": "home",
            "due_date": (today + timedelta(days=1)).strftime('%Y-%m-%d')
        },
        {
            "title": "Water plants",
            "description": "Water indoor and outdoor plants",
            "status": "completed",
            "priority": "low",
            "category": "home",
            "due_date": (today - timedelta(days=1)).strftime('%Y-%m-%d')
        },
        
        # Overdue tasks
        {
            "title": "Submit tax documents",
            "description": "Gather and submit required tax documents",
            "status": "pending",
            "priority": "high",
            "category": "urgent",
            "due_date": (today - timedelta(days=3)).strftime('%Y-%m-%d')
        },
        {
            "title": "Return library books",
            "description": "Books are overdue",
            "status": "pending",
            "priority": "medium",
            "category": "personal",
            "due_date": (today - timedelta(days=5)).strftime('%Y-%m-%d')
        },
        
        # Future tasks
        {
            "title": "Plan birthday party",
            "description": "Organize venue, guest list, and catering",
            "status": "pending",
            "priority": "low",
            "category": "personal",
            "due_date": (today + timedelta(days=30)).strftime('%Y-%m-%d')
        },
        {
            "title": "Annual performance review",
            "description": "Prepare self-assessment and goals for next year",
            "status": "pending",
            "priority": "medium",
            "category": "work",
            "due_date": (today + timedelta(days=45)).strftime('%Y-%m-%d')
        },
        {
            "title": "Vacation planning",
            "description": "Research and book summer vacation",
            "status": "pending",
            "priority": "low",
            "category": "personal",
            "due_date": (today + timedelta(days=60)).strftime('%Y-%m-%d')
        }
    ]
    
    return tasks


# ============================================================
# INJECTION FUNCTIONS
# ============================================================

def inject_tasks_via_api():
    """Inject tasks via API (recommended - tests validation)"""
    
    tasks = get_sample_tasks()
    
    print("\n" + "=" * 60)
    print("INJECTING TASKS VIA API")
    print("=" * 60 + "\n")
    
    # Check if API is running
    try:
        response = requests.get(BASE_URL, timeout=2)
        if response.status_code != 200:
            print("❌ API not responding")
            print("   Run: uvicorn main:app --reload")
            return
    except:
        print("❌ Cannot connect to API")
        print("   Run: uvicorn main:app --reload")
        return
    
    created = 0
    failed = 0
    
    for task in tasks:
        try:
            response = requests.post(f"{BASE_URL}/api/tasks", json=task, timeout=5)
            
            if response.status_code == 201:
                created += 1
               
                
            else:
                failed += 1
                print(f"❌ Failed: {task['title'][:40]} - {response.json().get('detail', 'Unknown error')}")
        
        except Exception as e:
            failed += 1
            print(f"❌ Error: {task['title'][:40]} - {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Created: {created}/{len(tasks)} tasks")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print("=" * 60 + "\n")


def inject_tasks_direct():
    """Inject tasks directly to database (faster)"""
    
    tasks = get_sample_tasks()
    
    connection = get_connection()
    cursor = connection.cursor()
    
    print("\n" + "=" * 60)
    print("INJECTING TASKS DIRECTLY TO DATABASE")
    print("=" * 60 + "\n")
    
    insert_statement = """
    INSERT INTO TASKS (title, description, status, priority, category, due_date, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """
    
    try:
        inserted = 0
        
        for task in tasks:
            params = (
                task['title'],
                task['description'],
                task['status'],
                task['priority'],
                task['category'],
                task['due_date']
            )
            
            cursor.execute(insert_statement, params)
            inserted += 1
            
           
        
        connection.commit()
        
        print("\n" + "=" * 60)
        print(f"✅ Inserted: {inserted}/{len(tasks)} tasks")
        print("=" * 60 + "\n")
        
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        connection.rollback()
    finally:
        connection.close()


# ============================================================
# MAIN MENU
# ============================================================

def show_menu():
    """Show menu"""
    print("\n" + "=" * 60)
    print("TASK MANAGEMENT - DATA POPULATION")
    print("=" * 60)
    print("\n📋 Options:")
    print("  1. Clear all tasks")
    print("  2. Inject tasks via API (recommended)")
    print("  3. Inject tasks directly to database")
    print("  4. Verify task data")
    print("  5. Show sample tasks")
    print("  6. Complete reset (clear + inject)")
    print("  0. Exit")
    print("\n" + "=" * 60)


def main():
    """Main menu"""
    while True:
        show_menu()
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            clear_all_tasks()
        elif choice == "2":
            inject_tasks_via_api()
        elif choice == "3":
            inject_tasks_direct()
        elif choice == "4":
            verify_tasks()
        elif choice == "5":
            show_sample_tasks()
        elif choice == "6":
            clear_all_tasks()
            inject_tasks_via_api()
        elif choice == "0":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid choice")


# ============================================================
# COMMAND LINE USAGE
# ============================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "clear":
            clear_all_tasks()
        elif command == "inject":
            inject_tasks_via_api()
        elif command == "direct":
            inject_tasks_direct()
        elif command == "verify":
            verify_tasks()
        elif command == "reset":
            clear_all_tasks()
            inject_tasks_via_api()
        else:
            print(f"❌ Unknown command: {command}")
            print("\nUsage:")
            print("  python populate_tasks.py clear   - Clear all tasks")
            print("  python populate_tasks.py inject  - Inject via API")
            print("  python populate_tasks.py direct  - Inject directly to DB")
            print("  python populate_tasks.py verify  - Verify data")
            print("  python populate_tasks.py reset   - Clear + inject")
    else:
        # Interactive menu
        main()