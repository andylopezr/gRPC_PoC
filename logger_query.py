import sqlite3
import argparse
from tabulate import tabulate 

def query_logs(db_path="/logs_data/logs.db", limit=20, event_type=None):
    """Query logs from the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        if event_type:
            cursor.execute(
                "SELECT id, event_type, details, timestamp FROM logs WHERE event_type = ? ORDER BY id DESC LIMIT ?", 
                (event_type, limit)
            )
        else:
            cursor.execute(
                "SELECT id, event_type, details, timestamp FROM logs ORDER BY id DESC LIMIT ?", 
                (limit,)
            )
            
        logs = cursor.fetchall()
        conn.close()
        
        if not logs:
            print("No logs found.")
            return
            
        headers = ["ID", "Event Type", "Details", "Timestamp"]
        print(tabulate(logs, headers=headers, tablefmt="grid"))
        print(f"Total: {len(logs)} logs")
        
    except Exception as e:
        print(f"Error querying logs: {e}")

def main():
    parser = argparse.ArgumentParser(description="Query logs from the logger database")
    parser.add_argument("--db", default="logs.db", help="Path to the database file")
    parser.add_argument("--limit", type=int, default=20, help="Limit the number of logs to retrieve")
    parser.add_argument("--type", help="Filter by event type")
    
    args = parser.parse_args()
    query_logs(args.db, args.limit, args.type)

if __name__ == "__main__":
    main()