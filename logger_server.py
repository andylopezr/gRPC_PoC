import grpc
from concurrent import futures
import logger_service_pb2, logger_service_pb2_grpc
import sqlite3
import os
from datetime import datetime

class LoggerService(logger_service_pb2_grpc.LoggerServiceServicer):
    def __init__(self, db_path="logs_data/logs.db"):
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
        
        # Store the database path
        self.db_path = db_path
        
        # Initialize the database
        self.init_database()
        
    def init_database(self):
        """Initialize the database by creating tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create logs table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            details TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
        
    def LogActivity(self, request, context):
        """Log activity to the database"""
        try:
            # Extract hash from details if present
            hash_end = request.details.split('-')[-1]
            print(hash_end)  # Keep original console print for debugging
            
            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert log entry
            cursor.execute(
                "INSERT INTO logs (event_type, details, timestamp) VALUES (?, ?, ?)",
                (request.event_type, request.details, timestamp)
            )
            
            # Commit changes and close connection
            conn.commit()
            conn.close()
            
            print(f"[LOG] {request.event_type}: {request.details}")
            return logger_service_pb2.LogResponse(logged=True)
            
        except Exception as e:
            print(f"Error logging to database: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {str(e)}")
            return logger_service_pb2.LogResponse(logged=False)
    
    def get_logs(self, limit=100):
        """Query logs from the database with a limit"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
            logs = cursor.fetchall()
            conn.close()
            return logs
        except Exception as e:
            print(f"Error querying logs: {e}")
            return []

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger_service = LoggerService()
    logger_service_pb2_grpc.add_LoggerServiceServicer_to_server(logger_service, server)
    server.add_insecure_port('[::]:50055')
    print("Logger server starting on port 50055")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()