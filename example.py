import grpc
import service_pb2
import service_pb2_grpc

def write_file(filename, content):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.FileServiceStub(channel)
        
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        request = service_pb2.FileRequest(
            filename=filename,
            content=content
        )
        
        response = stub.WriteFile(request)
        return response

response = write_file('example.txt', 'This is some example content')
print(f"Success: {response.success}")
print(f"Message: {response.message}")
print(f"File path: {response.file_path}")