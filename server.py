from concurrent import futures
import time
import grpc
import service_pb2
import service_pb2_grpc
from datetime import datetime
import os

UPLOAD_DIR = "uploaded_files"

class FileServicer(service_pb2_grpc.FileServiceServicer):
    def __init__(self):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    def SayHello(self, request, context):
        message = f"Hello, {request.name}!"
        return service_pb2.HelloReply(message=message)
    
    def GetServerTime(self, request, context):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return service_pb2.TimeResponse(timestamp=current_time)
    
    def WriteFile(self, request, context):
        try:
            filename = os.path.basename(request.filename)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            with open(file_path, 'wb') as f:
                f.write(request.content)
            
            return service_pb2.FileResponse(
                success=True,
                message=f"File {filename} written successfully",
                file_path=file_path
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return service_pb2.FileResponse(
                success=False,
                message=f"Error writing file: {str(e)}",
                file_path=""
            )
    
    def GetFilesList(self, request, context):
        try:
            files = os.listdir(UPLOAD_DIR)
            return service_pb2.FilesListResponse(filenames=files)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return service_pb2.FilesListResponse(filenames=[])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_FileServiceServicer_to_server(FileServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    print(f"Files will be stored in: {os.path.abspath(UPLOAD_DIR)}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()