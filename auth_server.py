import grpc
import uuid
from concurrent import futures
import auth_service_pb2, auth_service_pb2_grpc
import logger_service_pb2, logger_service_pb2_grpc

class AuthService(auth_service_pb2_grpc.AuthServiceServicer):
    def __init__(self):
        # LoggerService client setup
        self.logger_channel = grpc.insecure_channel('logger-service:50055')
        self.logger_stub = logger_service_pb2_grpc.LoggerServiceStub(self.logger_channel)
        self.active_sessions = {}  # Simple session storage

    def Login(self, request, context):
        # Authentication logic
        session_id = str(uuid.uuid4())
        self.active_sessions[session_id] = request.username
        
        # Log login event
        self.logger_stub.LogActivity(
            logger_service_pb2.LogRequest(
                event_type="SESSION_STARTED",
                details=f"User {request.username} logged in"
            )
        )
        
        return auth_service_pb2.AuthResponse(
            success=True,
            message="Login successful",
            session_id=session_id
        )

    def Logout(self, request, context):
        # Session termination logic
        username = self.active_sessions.pop(request.session_id, "unknown")
        
        # Log logout event
        self.logger_stub.LogActivity(
            logger_service_pb2.LogRequest(
                event_type="SESSION_TERMINATED",
                details=f"Session {request.session_id} ({username}) ended"
            )
        )
        
        return auth_service_pb2.AuthResponse(
            success=True,
            message="Logout successful"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50056') 
    server.start()
    print("Auth server started on port 50056")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()