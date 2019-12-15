import grpc
import upload_pb2
import upload_pb2_grpc
import threading
import io
import hashlib

CHUNK_SIZE = 1024 * 1024 * 4  # 4MB

def get_file_byte_chunks(f):
    while True:
        piece = f.read(CHUNK_SIZE)
        if len(piece) == 0:
            return
        yield upload_pb2.Chunk(content=piece)

class Client:
    def __init__(self, address):
            channel = grpc.insecure_channel(address)
            self.stub = upload_pb2_grpc.FileServerStub(channel)
    
    def upload(self, f, f_name):
        print("Inside here")
        hash_object = hashlib.sha1(f_name.encode())
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
        chunks_generator = get_file_byte_chunks(f)
        response = self.stub.upload(chunks_generator)
        
