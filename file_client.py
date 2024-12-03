import grpc
import file_service_pb2
import file_service_pb2_grpc
import os
from datetime import datetime

class FileClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = file_service_pb2_grpc.FileServiceStub(self.channel)
    
    def display_menu(self):
        print("\n=== gRPC File Service Client ===")
        print("1. Say Hello")
        print("2. Get Server Time")
        print("3. Upload File")
        print("4. Download File")
        print("5. List Files")
        print("6. Delete File")
        print("0. Exit")
        return input("Choose an option: ")
    
    def run_interactive(self):
        while True:
            try:
                choice = self.display_menu()
                
                if choice == '0':
                    print("Goodbye!")
                    break
                    
                elif choice == '1':
                    name = input("Enter your name: ")
                    response = self.stub.SayHello(file_service_pb2.HelloRequest(name=name))
                    print(f"Server response: {response.message}")
                
                elif choice == '2':
                    response = self.stub.GetServerTime(file_service_pb2.Empty())
                    print(f"Server time: {response.timestamp}")
                
                elif choice == '3':
                    file_path = input("Enter file path to upload: ")
                    if not os.path.exists(file_path):
                        print("Error: File not found!")
                        continue
                    
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    filename = os.path.basename(file_path)
                    request = file_service_pb2.FileRequest(
                        filename=filename,
                        content=content
                    )
                    response = self.stub.WriteFile(request)
                    print(f"Upload response: {response.message}")
                    if response.success:
                        print(f"File size: {response.file_size} bytes")
                        print(f"MD5 hash: {response.md5_hash}")
                
                elif choice == '4':
                    filename = input("Enter filename to download: ")
                    save_path = input("Enter save path: ")
                    
                    request = file_service_pb2.FileRequest(filename=filename)
                    response = self.stub.ReadFile(request)
                    
                    if response.success:
                        with open(save_path, 'wb') as f:
                            f.write(response.content)
                        print(f"File downloaded successfully to {save_path}")
                    else:
                        print(f"Error: {response.message}")
                
                elif choice == '5':
                    response = self.stub.GetFilesList(file_service_pb2.Empty())
                    if not response.files:
                        print("No files found")
                        continue
                        
                    print("\nFiles on server:")
                    print("-" * 80)
                    print(f"{'Filename':<30} {'Size':<10} {'Created':<20} {'MD5 Hash'}")
                    print("-" * 80)
                    
                    for file_info in response.files:
                        print(f"{file_info.filename:<30} {file_info.size:<10} {file_info.created_at:<20} {file_info.md5_hash}")
                
                elif choice == '6':
                    filename = input("Enter filename to delete: ")
                    confirm = input(f"Are you sure you want to delete {filename}? (y/N): ")
                    
                    if confirm.lower() == 'y':
                        request = file_service_pb2.FileRequest(filename=filename)
                        response = self.stub.DeleteFile(request)
                        print(f"Delete response: {response.message}")
                    else:
                        print("Delete cancelled")
                
                else:
                    print("Invalid option, please try again")
                
                input("\nPress Enter to continue...")
                
            except grpc.RpcError as e:
                print(f"RPC Error: {e.details()}")
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"Error: {str(e)}")
                input("\nPress Enter to continue...")

def main():
    client = FileClient()
    try:
        client.run_interactive()
    except KeyboardInterrupt:
        print("\nShutting down client...")

if __name__ == "__main__":
    main()