from concurrent import futures
import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
import rx
from rx import operators as ops

class FileTransferService(file_transfer_pb2_grpc.FileTransferServiceServicer):
    def Upload(self, request_iterator, context):
        # 파일 스트림을 비동기적으로 처리하기 위해 RxPy 사용
        rx.from_(request_iterator).pipe(
            ops.map(lambda file_chunk: file_chunk.data),
            ops.reduce(lambda acc, x: acc + x, b'')
        ).subscribe(
            on_next=lambda file_bytes: self.save_file(file_bytes),
            on_error=lambda e: print(f"Error: {e}"),
            on_completed=lambda: print("File upload completed.")
        )
        return file_transfer_pb2.UploadStatus(message="File uploaded successfully.")

    def save_file(self, file_bytes):
        print(f"Received: {len(file_bytes)}")
        with open("received_file", "wb") as f:
            f.write(file_bytes)
        print("File saved.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServiceServicer_to_server(FileTransferService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

