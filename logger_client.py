import grpc
import logger_service_pb2, logger_service_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50055')
    stub = logger_service_pb2_grpc.LoggerServiceStub(channel)
    
    # Test logging
    log_response = stub.LogActivity(logger_service_pb2.LogRequest(
        event_type="AUTH_EVENT",
        details="User 'user1' logged in"
    ))
    print(f"Logging succeeded: {log_response.logged}")

if __name__ == '__main__':
    run()