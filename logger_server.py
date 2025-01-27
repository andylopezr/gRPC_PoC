import grpc
from concurrent import futures
import logger_service_pb2, logger_service_pb2_grpc

class LoggerService(logger_service_pb2_grpc.LoggerServiceServicer):
    def LogActivity(self, request, context):
        # Logging logic only
        print(f"[LOG] {request.event_type}: {request.details}")
        return logger_service_pb2.LogResponse(logged=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger_service_pb2_grpc.add_LoggerServiceServicer_to_server(LoggerService(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()