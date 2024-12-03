from concurrent import futures
import grpc
import file_service_pb2
import file_service_pb2_grpc
from datetime import datetime
import os

UPLOAD_DIR = "uploaded_files"

class FileServicer(file_service_pb2_grpc.FileServiceServicer):
    def __init__(self):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    def SayHello(self, request, context):
        message = f"Hello, {request.name}!"
        return file_service_pb2.HelloResponse(message=message)
    
    def GetServerTime(self, request, context):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return file_service_pb2.TimeResponse(timestamp=current_time)
    
    def WriteFile(self, request, context):
        try:
            filename = os.path.basename(request.filename)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            with open(file_path, 'wb') as f:
                f.write(request.content)
            
            return file_service_pb2.FileResponse(
                success=True,
                message=f"File {filename} written successfully",
                file_path=file_path
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return file_service_pb2.FileResponse(
                success=False,
                message=f"Error writing file: {str(e)}",
                file_path=""
            )
    
    def GetFilesList(self, request, context):
        try:
            files = os.listdir(UPLOAD_DIR)
            return file_service_pb2.FilesListResponse(filenames=files)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return file_service_pb2.FilesListResponse(filenames=[])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("File Service started on port 50051")
    print(f"Files will be stored in: {os.path.abspath(UPLOAD_DIR)}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()