# streaming_server.py
from concurrent import futures
import time
import grpc
import streaming_service_pb2
import streaming_service_pb2_grpc
from datetime import datetime
import os
import queue
import threading

UPLOAD_DIR = "streamed_files"
CHUNK_SIZE = 1024 * 1024  # 1MB chunks

class StreamingServicer(streaming_service_pb2_grpc.StreamingServiceServicer):
    def __init__(self):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        self.client_queues = {}
        self.client_queues_lock = threading.Lock()
        self.client_counter = 0  # Counter for client numbering

    def get_next_client_number(self):
        with self.client_queues_lock:
            self.client_counter += 1
            return self.client_counter

    def StreamServerTime(self, request, context):
        try:
            while context.is_active():
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield streaming_service_pb2.TimeResponse(timestamp=current_time)
                time.sleep(1)
        except Exception as e:
            print(f"StreamServerTime error: {e}")

    def StreamUploadFile(self, request_iterator, context):
        try:
            current_file = None
            file_handle = None
            
            for chunk in request_iterator:
                if file_handle is None:
                    current_file = os.path.basename(chunk.filename)
                    file_path = os.path.join(UPLOAD_DIR, current_file)
                    file_handle = open(file_path, 'wb')

                file_handle.write(chunk.chunk_data)

                if chunk.is_last_chunk:
                    file_handle.close()
                    return streaming_service_pb2.FileResponse(
                        success=True,
                        message=f"File {current_file} uploaded successfully",
                        file_path=file_path
                    )

        except Exception as e:
            if file_handle:
                file_handle.close()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return streaming_service_pb2.FileResponse(
                success=False,
                message=f"Error uploading file: {str(e)}",
                file_path=""
            )

    def ChatStream(self, request_iterator, context):
        # Assign a number to this client
        client_number = self.get_next_client_number()
        client_queue = queue.Queue()
        client_id = id(context)

        # Store client info
        with self.client_queues_lock:
            self.client_queues[client_id] = {
                'queue': client_queue,
                'number': client_number
            }

            # Send system message about new client
            system_message = streaming_service_pb2.ChatMessage(
                sender="System",
                message=f"Client({client_number}) has joined the chat",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            for client_info in self.client_queues.values():
                client_info['queue'].put(system_message)

            def cleanup():
                with self.client_queues_lock:
                    if client_id in self.client_queues:
                        leaving_number = self.client_queues[client_id]['number']
                        # Send system message about client leaving
                        leave_message = streaming_service_pb2.ChatMessage(
                            sender="System",
                            message=f"Client({leaving_number}) has left the chat",
                            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        for cid, client_info in self.client_queues.items():
                            if cid != client_id:  # Don't send to leaving client
                                client_info['queue'].put(leave_message)
                        del self.client_queues[client_id]

            context.add_callback(cleanup)

        try:
            def handle_client_messages():
                for message in request_iterator:
                    # Add client number to sender
                    message.sender = f"Client({client_number})"
                    # Broadcast to all clients
                    with self.client_queues_lock:
                        for client_info in self.client_queues.values():
                            client_info['queue'].put(message)

            client_thread = threading.Thread(target=handle_client_messages)
            client_thread.start()

            while context.is_active():
                try:
                    message = client_queue.get(timeout=1.0)
                    yield message
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error yielding message: {e}")
                    break

        except Exception as e:
            print(f"ChatStream error for Client({client_number}): {e}")
        finally:
            with self.client_queues_lock:
                if client_id in self.client_queues:
                    del self.client_queues[client_id]

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_service_pb2_grpc.add_StreamingServiceServicer_to_server(
        StreamingServicer(), server
    )
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Streaming Service started on port 50053")
    print(f"Streamed files will be stored in: {os.path.abspath(UPLOAD_DIR)}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()