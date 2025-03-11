FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Generate gRPC code
RUN python -m pip install grpcio-tools && \
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/file_service.proto && \
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/streaming_service.proto && \
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/random_service.proto && \
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/auth_service.proto && \
    python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/logger_service.proto

# Create directories for uploaded files
RUN mkdir -p uploaded_files streamed_files

# Default command (can be overridden in docker-compose)
CMD ["python", "file_server.py"]