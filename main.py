import sys
import argparse
from sync_service import SyncService

def main():
    parser = argparse.ArgumentParser(description="Sync tasks from Things 3 to Tana.")
    parser.add_argument("scope", choices=["inbox", "today", "all"], nargs="?", default="today", help="Scope to sync (default: today)")
    
    args = parser.parse_args()
    
    service = SyncService()
    
    if args.scope == "inbox":
        service.sync_inbox()
    elif args.scope == "today":
        service.sync_today()
    elif args.scope == "all":
        service.sync_inbox()
        service.sync_today()
    
if __name__ == "__main__":
    main()
