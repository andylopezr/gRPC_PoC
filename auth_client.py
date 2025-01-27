import grpc
import auth_service_pb2, auth_service_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50054')
    stub = auth_service_pb2_grpc.AuthServiceStub(channel)
    
    # Test login
    login_response = stub.Login(auth_service_pb2.LoginRequest(
        username="user1", password="pass123"
    ))
    print(f"Auth Response: {login_response.message}")

if __name__ == '__main__':
    run()