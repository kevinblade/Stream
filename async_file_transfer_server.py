import time
import secrets
import grpc
import asyncio
import file_transfer_pb2
import file_transfer_pb2_grpc

class FileTransferService(file_transfer_pb2_grpc.FileTransferServiceServicer):

    async def Upload(self, request_iterator, context):
        file_bytes = b''
        start_time = time.time()
        async for file_chunk in request_iterator:
            file_bytes += file_chunk.data
        # 비동기 파일 저장
        await self.save_file(file_bytes)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"작업 수행에 걸린 CPU 시간: {elapsed_time}초")
        return file_transfer_pb2.UploadStatus(message="File uploaded successfully.")

    async def save_file(self, file_bytes):
        # 4바이트 길이의 보안 강한 랜덤 텍스트 문자열 생성
        random_id = secrets.token_hex(4)
        with open(f"received_file_{random_id}", "wb") as f:
            f.write(file_bytes)
        print("File saved.")

async def serve():
    server = grpc.aio.server()
    file_transfer_pb2_grpc.add_FileTransferServiceServicer_to_server(FileTransferService(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f"Starting server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())

