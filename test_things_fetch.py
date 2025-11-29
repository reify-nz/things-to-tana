from things_provider import ThingsProvider
import json

def main():
    provider = ThingsProvider()
    
    print("--- Testing Things 3 Data Fetch ---")
    
    print("\nFetching Inbox Tasks...")
    try:
        inbox_tasks = provider.get_inbox_tasks()
        print(f"Found {len(inbox_tasks)} tasks in Inbox.")
        for task in inbox_tasks[:3]: # Print first 3
            print(f" - {task.get('title')} ({task.get('uuid')})")
        if len(inbox_tasks) > 3:
            print(" ...")
    except Exception as e:
        print(f"Error fetching Inbox: {e}")

    print("\nFetching Today Tasks...")
    try:
        today_tasks = provider.get_today_tasks()
        print(f"Found {len(today_tasks)} tasks in Today.")
        for task in today_tasks[:3]: # Print first 3
            print(f" - {task.get('title')} ({task.get('uuid')})")
        if len(today_tasks) > 3:
            print(" ...")
    except Exception as e:
        print(f"Error fetching Today: {e}")

if __name__ == "__main__":
    main()
