import grpc
import signal
import sys
import auth_service_pb2, auth_service_pb2_grpc

class AuthClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50054')
        self.stub = auth_service_pb2_grpc.AuthServiceStub(self.channel)
        self.session_id = None
        
    def login(self, username, password):
        # Perform login
        login_response = self.stub.Login(auth_service_pb2.LoginRequest(
            username=username, 
            password=password
        ))
        self.session_id = login_response.session_id.split('-')[-1]
        print(f"Login: {login_response.message} (Session ID: {login_response.session_id})")
        
    def logout(self):
        if self.session_id:
            # Perform logout
            logout_response = self.stub.Logout(auth_service_pb2.LogoutRequest(
                session_id=self.session_id
            ))
            print(f"Logout: {logout_response.message}")
            self.session_id = None
            
    def cleanup(self, signum, frame):
        print("\nReceived shutdown signal. Logging out...")
        self.logout()
        sys.exit(0)

def run():
    client = AuthClient()
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, client.cleanup)
    
    try:
        # Perform login
        client.login("user1", "pass123")
        
        print("\nSession active. Press Ctrl+C to logout and exit.")
        # Keep the session alive until Ctrl+C
        signal.pause()
        
    except KeyboardInterrupt:
        # fallback
        client.cleanup(None, None)

if __name__ == '__main__':
    run()