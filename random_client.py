import grpc
import random_service_pb2
import random_service_pb2_grpc

def stream_random_numbers(stub, min_val, max_val, count, delay):
    """
    Request and display streaming random numbers from the server
    """
    try:
        request = random_service_pb2.RandomNumberRequest(
            min=min_val,
            max=max_val,
            count=count,
            delay=delay
        )
        
        responses = stub.GetRandomNumbers(request)
        
        print("\nReceiving random numbers:")
        print("Sequence | Number | Timestamp")
        print("-" * 35)
        
        for response in responses:
            print(f"{response.sequence:^8} | {response.number:^6} | {response.timestamp}")
            
    except grpc.RpcError as e:
        print(f"RPC error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def run_client():
    # Note the port change to match the random number server
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = random_service_pb2_grpc.RandomNumberServiceStub(channel)
        
        print("Random Number Streaming Client")
        print("-----------------------------")
        
        try:
            min_val = int(input("Enter minimum value: "))
            max_val = int(input("Enter maximum value: "))
            count = int(input("Enter how many numbers to generate: "))
            delay = int(input("Enter delay between numbers (milliseconds): "))
            
            stream_random_numbers(stub, min_val, max_val, count, delay)
            
        except ValueError as e:
            print(f"ValueError occurred: {e}")
        except KeyboardInterrupt:
            print("\nClient terminated by user")

if __name__ == '__main__':
    run_client()