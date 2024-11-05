import grpc
import file_service_pb2
import file_service_pb2_grpc

def run_client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        
        # Test SayHello
        response = stub.SayHello(file_service_pb2.HelloRequest(name="gRPC User"))
        print(f"Greeter client received: {response.message}")
        
        # Test GetServerTime
        time_response = stub.GetServerTime(file_service_pb2.Empty())
        print(f"Server time: {time_response.timestamp}")
        
        # Test WriteFile
        test_content = b"Hello, this is a test file content!"
        file_request = file_service_pb2.FileRequest(
            filename="test.txt",
            content=test_content
        )
        file_response = stub.WriteFile(file_request)
        print(f"File write response: {file_response.message}")
        print(f"File path: {file_response.file_path}")
        
        # Test GetFilesList
        files_response = stub.GetFilesList(file_service_pb2.Empty())
        print("Files in upload directory:")
        for filename in files_response.filenames:
            print(f"- {filename}")

if __name__ == "__main__":
    run_client()