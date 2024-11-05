# streaming_client.py
import grpc
import streaming_service_pb2
import streaming_service_pb2_grpc
import threading
import os
import queue
from datetime import datetime

def get_server_time_stream(stub):
    try:
        time_stream = stub.StreamServerTime(streaming_service_pb2.Empty())
        for response in time_stream:
            print(f"Server time: {response.timestamp}")
    except grpc.RpcError as e:
        print(f"Stream error: {e}")

def upload_file_stream(stub, filepath):
    try:
        chunk_iterator = get_file_chunks(filepath)
        response = stub.StreamUploadFile(chunk_iterator)
        print(f"Upload response: {response.message}")
        print(f"File path: {response.file_path}")
    except grpc.RpcError as e:
        print(f"Upload error: {e}")

def get_file_chunks(filepath):
    CHUNK_SIZE = 1024 * 1024  # 1MB chunks
    filename = os.path.basename(filepath)
    
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                yield streaming_service_pb2.FileChunk(
                    filename=filename,
                    chunk_data=b'',
                    is_last_chunk=True
                )
                break
            
            yield streaming_service_pb2.FileChunk(
                filename=filename,
                chunk_data=chunk,
                is_last_chunk=False
            )

def message_iterator(message_queue):
    while True:
        message = message_queue.get()
        if message is None:
            break
        yield message

def chat_stream(stub):
    try:
        message_queue = queue.Queue()
        chat_stream = stub.ChatStream(message_iterator(message_queue))
        
        def receive_messages():
            try:
                for message in chat_stream:
                    if message.sender == "System":
                        print(f"\n[{message.timestamp}] {message.message}")
                    else:
                        print(f"\n[{message.timestamp}] {message.sender}: {message.message}")
            except grpc.RpcError as e:
                print(f"Receive error: {e}")

        receive_thread = threading.Thread(target=receive_messages, daemon=True)
        receive_thread.start()

        try:
            while True:
                message = input("Enter message (or 'quit' to exit): ")
                if message.lower() == 'quit':
                    break

                chat_message = streaming_service_pb2.ChatMessage(
                    sender="",  # Server will set the correct client number
                    message=message,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                message_queue.put(chat_message)

        finally:
            message_queue.put(None)
            receive_thread.join(timeout=1)

    except grpc.RpcError as e:
        print(f"Chat error: {e}")
    except Exception as e:
        print(f"General error: {e}")

def run_client():
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = streaming_service_pb2_grpc.StreamingServiceStub(channel)

        print("\n1. Server Streaming - Time Updates")
        print("Press Ctrl+C to stop time updates")
        try:
            get_server_time_stream(stub)
        except KeyboardInterrupt:
            print("\nTime updates stopped")

        print("\n2. Client Streaming - File Upload")
        file_path = input("Enter file path to upload (or press Enter to skip): ")
        if file_path:
            upload_file_stream(stub, file_path)

        print("\n3. Bidirectional Streaming - Chat")
        chat_stream(stub)

if __name__ == "__main__":
    run_client()