from concurrent import futures
import threading
import grpc
import storage_pb2
import storage_pb2_grpc
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Listener(storage_pb2_grpc.FileServerServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self):
        print('initialization')

    def upload_chunk_stream(self, request, context):
        for c in request:
            print(c.chunk)
        return storage_pb2.ResponseBoolean(success = False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_pb2_grpc.add_FileServerServicer_to_server(
        Listener(), server)
    server.add_insecure_port('[::]:9999')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()