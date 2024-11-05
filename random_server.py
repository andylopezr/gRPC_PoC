from concurrent import futures
import time
import grpc
import random_service_pb2
import random_service_pb2_grpc
from datetime import datetime
import random

class RandomNumberServicer(random_service_pb2_grpc.RandomNumberServiceServicer):
    def GetRandomNumbers(self, request, context):
        """
        Stream random numbers based on client request parameters.
        """
        try:
            for i in range(request.count):
                number = random.randint(request.min, request.max)
                response = random_service_pb2.RandomNumberResponse(
                    number=number,
                    sequence=i + 1,
                    timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3]
                )
                yield response
                time.sleep(request.delay / 1000)
                
        except Exception as e:
            print(f"Error in GetRandomNumbers: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    random_service_pb2_grpc.add_RandomNumberServiceServicer_to_server(
        RandomNumberServicer(), server
    )
    # Use a different port than your existing service
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Random Number Server started on port 50052")
    print("Waiting for client requests...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()