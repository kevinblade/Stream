import time
import grpc
import asyncio
import file_transfer_pb2
import file_transfer_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = file_transfer_pb2_grpc.FileTransferServiceStub(channel)
        start_time = time.time()

        async def generate_chunks():
            with open("file_to_upload", "rb") as f:
                while (chunk := f.read(2048 * 1024)):
                    yield file_transfer_pb2.FileChunk(data=chunk)
        response = await stub.Upload(generate_chunks())
        print(response.message)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"작업 수행에 걸린 CPU 시간: {elapsed_time}초")

if __name__ == '__main__':
    asyncio.run(run())

