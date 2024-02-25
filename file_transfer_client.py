import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = file_transfer_pb2_grpc.FileTransferServiceStub(channel)
    # 파일을 청크로 나누어 전송
    def generate_chunks():
        with open("file_to_upload", "rb") as f:
            while chunk := f.read(1024):  # 1KB 크기의 청크로 읽기
                yield file_transfer_pb2.FileChunk(data=chunk)
    response = stub.Upload(generate_chunks())
    print(response.message)

if __name__ == '__main__':
    run()

