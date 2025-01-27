import grpc
from concurrent import futures
import auth_service_pb2, auth_service_pb2_grpc

class AuthService(auth_service_pb2_grpc.AuthServiceServicer):
    def Login(self, request, context):
        # Authentication logic only
        return auth_service_pb2.AuthResponse(
            success=True,
            message=f"Logged in as {request.username}"
        )

    def Logout(self, request, context):
        # Session termination only
        return auth_service_pb2.AuthResponse(
            success=True,
            message=f"Session {request.session_id} terminated"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()