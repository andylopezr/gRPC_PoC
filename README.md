# gRPC Python Services Demo

This project demonstrates various gRPC implementations in Python, featuring both basic operations and streaming capabilities. It includes multiple services with a new **SRP (Single Responsibility Principle)** example for authentication and logging.

# Docker Implementation

This project can be containerized using Docker for easy deployment and consistent execution across environments.

## Project Structure

```
grpc_project/
├── protos/
│ ├── file_service.proto # Basic file operations proto
│ ├── random_service.proto # Random number service proto
│ ├── streaming_service.proto # Streaming operations proto
│ ├── auth_service.proto # New: Authentication service proto
│ └── logger_service.proto # New: Logging service proto
├── file_client.py # Basic file operations client
├── file_server.py # Basic file operations server
├── streaming_client.py # Streaming operations client
├── streaming_server.py # Streaming operations server
├── random_client.py # Random number client
├── random_server.py # Random number server
├── auth_server.py # New: Auth service server
├── auth_client.py # New: Auth service client
├── logger_server.py # New: Logger service server
├── logger_client.py # New: Logger service client
├── logger_query.py # New: Log database query tool
├── Dockerfile # For building service images
├── docker-compose.yml # For orchestrating multiple services
├── requirements.txt ├── uploaded_files/ # For basic file service
├── streamed_files/ # For streaming service
└── logs_data/ # For persistent database storage
```

## Additional Dependencies

```bash
pip install tabulate
```

## Features

### 1. Basic File Service (Port 50051)

- Simple greeting service
- Get server time
- Write files
- List uploaded files

### 2. Streaming Service (Port 50053)

- Server streaming (continuous time updates)
- Client streaming (chunked file upload)
- Bidirectional streaming (chat system)
  - Numbered client identifiers (Client(1), Client(2), etc.)
  - Join/Leave notifications
  - Real-time message broadcasting

### 3. Random Number Service (Port 50052)

- Server streaming of random numbers
- Configurable range and interval
- Sequence tracking

### 4. SRP Example: Authentication & Logging (Ports 50054/50055) [NEW]

- **AuthService**: Dedicated to user authentication (login/logout)
- **LoggerService**: Dedicated to activity logging
- Demonstrates Single Responsibility Principle:
  - AuthService changes only for authentication rules
  - LoggerService changes only for logging formats/storage

### Logging Service (LoggerService)

The LoggerService demonstrates SRP by handling only logging responsibilities:

- Event logging for system activities with persistent SQLite database storage
- No authentication logic
- Easily extendable logging format
- Clear separation of concerns
- Query capabilities for retrieving log history

Example log entries:

```bash
[LOG] SESSION_STARTED: User 'user1' logged in [LOG] SESSION_TERMINATED: Session 550e8400-e29b-41d4-a716-446655440000 (user1) ended
```

### Database Features

The LoggerService now includes a SQLite database implementation:

- Logs are stored persistently in `logs.db`
- Each log entry includes:
  - ID (auto-incrementing)
  - Event type
  - Details
  - Timestamp
- Log records survive across server restarts

### Query Tool

A command-line query tool is available to search and display logs:

```bash
# View recent logs (default: 20 entries)
python logger_query.py

# Customize output
python logger_query.py --limit 50
python logger_query.py --type SESSION_STARTED
python logger_query.py --db custom_logs.db
```

The query tool displays logs in a well-formatted table with:

- ID
- Event Type
- Details
- Timestamp

## Setup Instructions

1. **Install Dependencies**

```bash
pip install grpcio grpcio-tools
```

2. **Generate gRPC Code**

```bash
# For file service
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/file_service.proto

# For streaming service
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/streaming_service.proto

# For random number service
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/random_service.proto

# For new SRP example services
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/auth_service.proto
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/logger_service.proto
```

## Running the Services

### 1. Basic File Service

```bash
# Terminal 1 - Start server
python file_server.py

# Terminal 2 - Run client
python file_client.py
```

### 2. Streaming Service

```bash
# Terminal 1 - Start server
python streaming_server.py

# Terminal 2+ - Run multiple clients
python streaming_client.py
```

### 3. Random Number Service

```bash
# Terminal 1 - Start server
python random_server.py

# Terminal 2 - Run client
python random_client.py
```

### 4. SRP Example: Auth & Logging Services [NEW]

```bash
# Terminal 1 - Start Logger Service (Port 50055)
python logger_server.py

# Terminal 2 - Start Auth Service (Port 50054)
python auth_server.py

# Terminal 3 - Run Auth Client
python auth_client.py
# Expected output: "Login: Login successful (Session ID: [uuid])"
# Press Ctrl+C to logout
```

## Streaming Service Features in Detail

### Server Streaming - Time Updates

- Continuous server time updates
- Press Ctrl+C to stop receiving updates

```python
# Example output
Server time: 14:25:30.123
Server time: 14:25:31.124
Server time: 14:25:32.125
```

### Client Streaming - File Upload

- Large file handling with chunked upload
- Progress tracking
- Automatic chunk size management (1MB chunks)

```python
# Example usage
Enter file path to upload: example.txt
Upload response: File example.txt uploaded successfully
File path: streamed_files/example.txt
```

### Bidirectional Streaming - Chat System

- Automatic client numbering
- System notifications for client join/leave
- Real-time message broadcasting

Example chat session:

```
[14:30:00] Client(1) has joined the chat
[14:30:05] Client(2) has joined the chat
[14:30:10] Client(1): Hello everyone!
[14:30:15] Client(2): Hi there!
[14:30:20] Client(1) has left the chat
```

Features:

- Each client gets a unique identifier (Client(1), Client(2), etc.)
- System messages for client join/leave events
- Timestamp for each message
- Clean disconnection handling
- Thread-safe message broadcasting

## Implementation Details

### Server-side Features

- Thread-safe client management
- Proper message queuing
- Clean disconnection handling
- Automatic client numbering
- System message broadcasting

### Client-side Features

- Interactive command interface
- Proper error handling
- Clean shutdown process
- Separate threads for sending/receiving messages
- Format-friendly message display

## Error Handling

The services handle various error scenarios:

- Network disconnections
- Invalid file paths
- Server unavailability
- Client disconnections
- Thread interruptions

## SRP Example Features in Detail

### Authentication Service (AuthService)

The AuthService demonstrates the Single Responsibility Principle by focusing solely on authentication:

- User login/logout management
- Session tracking with UUIDs
- Clean separation from logging concerns
- Graceful shutdown with Ctrl+C handling

Example auth flow:

```
# Terminal output when running auth_client.py
Login: Login successful (Session ID: 550e8400-e29b-41d4-a716-446655440000)
Session active. Press Ctrl+C to logout and exit.
Received shutdown signal. Logging out...
Logout: Logout successful
```

### Logging Service (LoggerService)

The LoggerService demonstrates SRP by handling only logging responsibilities:

- Event logging for system activities
- No authentication logic
- Easily extendable logging format
- Clear separation of concerns

Example log entries:

```
# Logger server output
[LOG] SESSION_STARTED: User 'user1' logged in
[LOG] SESSION_TERMINATED: Session 550e8400-e29b-41d4-a716-446655440000 (user1) ended
```

### Interaction Flow

```
Auth Client → AuthService → LoggerService
    │         (authentication)  (logging)
    └─────────── Ctrl+C ─────────────────┘
        (triggers logout & logging)
```

## Usage Notes

1. **Starting Multiple Chat Clients**

   - Each new client automatically gets the next available number
   - Clients are notified when others join or leave
   - Messages show client numbers for easy identification

2. **File Operations**

   - Basic service: Single file upload
   - Streaming service: Chunked file upload for large files
   - Separate directories for each service

3. **Time Updates**
   - Basic service: Single time request
   - Streaming service: Continuous updates

## Common Use Cases

1. **File Transfer**

   - Large file uploads
   - Progress monitoring
   - File listing and management

2. **Real-time Updates**

   - Server time synchronization
   - Continuous data streaming
   - Event notifications

3. **Chat System**
   - Team communication
   - System notifications
   - Multi-client interaction

## Testing the Services

1. **Basic Operations**

```bash
python file_client.py
# Follow the prompts for basic operations
```

2. **Streaming Chat**

```bash
# Start multiple instances:
python streaming_client.py
# Skip time updates with Ctrl+C
# Skip file upload with Enter
# Start chatting with automatically assigned client numbers
```

3. **Random Numbers**

```bash
python random_client.py
# Follow the prompts to configure random number generation
```
