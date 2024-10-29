# gRPC Python Proof of Concept

This project demonstrates a basic gRPC implementation in Python, featuring both unary calls and file operations. It includes a server that can handle basic greeting messages, provide server time, and manage file operations, along with a client that can interact with these services.

## Project Structure

```
grpc_poc/
├── protos/
│   └── service.proto      # Protocol Buffer service definitions
├── service_pb2.py        # Generated Protocol Buffer code
├── service_pb2_grpc.py   # Generated gRPC code
├── server.py             # Server implementation
├── client.py             # Client implementation
└── requirements.txt      # Project dependencies
```

## Features

The PoC implements the following RPC methods:

1. **SayHello**
   - Simple greeting service
   - Takes a name as input and returns a greeting message

2. **GetServerTime**
   - Returns the current server timestamp
   - Demonstrates simple no-input RPC calls

3. **WriteFile**
   - Allows uploading files to the server
   - Handles both text and binary files
   - Includes safety features like filename sanitization
   - Returns status, message, and file path

4. **GetFilesList**
   - Lists all files in the upload directory
   - Demonstrates server-side directory operations

## Protocol Buffer Definition

The `service.proto` file defines the service interface using Protocol Buffers. Key message types include:

- `HelloRequest/HelloReply`: For basic greeting service
- `Empty`: For requests that don't need parameters
- `TimeResponse`: For server time responses
- `FileRequest`: Contains filename and file content
- `FileResponse`: Contains operation status and details
- `FilesListResponse`: Contains list of uploaded files

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install grpcio grpcio-tools
   ```

2. **Generate gRPC Code**
   ```bash
   python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/service.proto
   ```
   This command generates:
   - `service_pb2.py`: Contains Protocol Buffer message classes
   - `service_pb2_grpc.py`: Contains gRPC service classes

3. **Start the Server**
   ```bash
   python server.py
   ```
   The server will:
   - Create an `uploaded_files` directory if it doesn't exist
   - Listen on port 50051
   - Handle incoming RPC requests

4. **Run the Client**
   ```bash
   python client.py
   ```

## Implementation Details

### Server (`server.py`)

The server implements the `FileServicer` class which provides:

1. **Initialization**
   - Creates upload directory
   - Sets up gRPC server with thread pool

2. **Service Methods**
   - `SayHello`: Simple greeting implementation
   - `GetServerTime`: Returns formatted current time
   - `WriteFile`: 
     - Handles file writing operations
     - Includes safety checks
     - Provides detailed operation status
   - `GetFilesList`: Directory listing implementation

3. **Safety Features**
   - Filename sanitization to prevent directory traversal
   - Exception handling for all operations
   - Dedicated upload directory
   - Thread-safe file operations

### Client (`client.py`)

The client demonstrates:

1. **Connection Management**
   - Uses context manager for channel handling
   - Connects to localhost:50051

2. **Service Calls**
   - Shows how to call each service method
   - Handles responses and prints results
   - Demonstrates different parameter types

3. **File Operations**
   - Shows how to send file content
   - Handles both text and binary data
   - Processes operation responses

## Security Considerations

1. **File Operations**
   - Filename sanitization prevents directory traversal attacks
   - Dedicated upload directory contains file operations
   - Error handling prevents information leakage

2. **Network Security**
   - Uses insecure channel for demonstration
   - Should be upgraded to secure channel (TLS) for production

## Error Handling

- Server-side error handling with proper gRPC status codes
- Client receives detailed error messages
- File operation failures are properly reported
- Network errors are caught and handled

## Usage Examples

### Basic Greeting
```python
# Client code
response = stub.SayHello(service_pb2.HelloRequest(name="User"))
print(response.message)
```

### File Upload
```python
# Client code
with open('myfile.txt', 'rb') as f:
    content = f.read()
    request = service_pb2.FileRequest(
        filename="myfile.txt",
        content=content
    )
    response = stub.WriteFile(request)
```

### List Files
```python
# Client code
response = stub.GetFilesList(service_pb2.Empty())
for filename in response.filenames:
    print(filename)
```