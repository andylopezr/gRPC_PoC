from concurrent import futures
import grpc
import file_service_pb2
import file_service_pb2_grpc
from datetime import datetime
import os
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

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
    
    def _compute_file_hash(self, content):
        return hashlib.sha256(content).hexdigest()
    
    def WriteFile(self, request, context):
        try:
            filename = os.path.basename(request.filename)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            with open(file_path, 'wb') as f:
                f.write(request.content)
            
            file_hash = self._compute_file_hash(request.content)

            return file_service_pb2.FileResponse(
                success=True,
                message=f"File {filename} written successfully",
                file_path=file_path,
                file_size=len(request.content),
                hash=file_hash 
            )
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return file_service_pb2.FileResponse(
                success=False,
                message=f"Error writing file: {str(e)}",
                file_path="",
                file_size=0,
                hash=""
            )
    
    def ReadFile(self, request, context):
        try:
            filename = os.path.basename(request.filename)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            if not os.path.exists(file_path):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"File {filename} not found")
                return file_service_pb2.FileContentResponse(
                    success=False,
                    content=b"",
                    message=f"File {filename} not found"
                )
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            return file_service_pb2.FileContentResponse(
                success=True,
                content=content,
                message=f"File {filename} read successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return file_service_pb2.FileContentResponse(
                success=False,
                content=b"",
                message=f"Error reading file: {str(e)}"
            )
    
    def DeleteFile(self, request, context):
        try:
            filename = os.path.basename(request.filename)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            if not os.path.exists(file_path):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"File {filename} not found")
                return file_service_pb2.FileResponse(
                    success=False,
                    message=f"File {filename} not found",
                    file_path=""
                )
            
            os.remove(file_path)
            return file_service_pb2.FileResponse(
                success=True,
                message=f"File {filename} deleted successfully",
                file_path=file_path
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return file_service_pb2.FileResponse(
                success=False,
                message=f"Error deleting file: {str(e)}",
                file_path=""
            )
    
    def GetFilesList(self, request, context):
        try:
            files = []
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                file_stat = os.stat(file_path)
                with open(file_path, 'rb') as f:
                    content = f.read()
                    file_hash = hashlib.sha256(content).hexdigest()
                
                files.append(file_service_pb2.FileInfo(
                    filename=filename,
                    size=file_stat.st_size,
                    created_at=datetime.fromtimestamp(file_stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    modified_at=datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    hash=file_hash 
                ))
            return file_service_pb2.FilesListResponse(files=files)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return file_service_pb2.FilesListResponse(files=[])

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