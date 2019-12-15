import grpc
import storage_pb2
import storage_pb2_grpc
import threading
import io
import hashlib

CHUNK_SIZE = 1024 * 1024 * 4  # 4MB

def get_file_byte_chunks(f):
    while True:
        piece = f.read(CHUNK_SIZE)
        if len(piece) == 0:
            return
        yield storage_pb2.ChunkRequest(chunk=piece)

class Client:
    def __init__(self, address):
            channel = grpc.insecure_channel(address)
            self.stub = storage_pb2_grpc.FileServerStub(channel)
    
    def upload(self, f, f_name):
        print("Inside here")
        hash_object = hashlib.sha1(f_name.encode())
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
        chunks_generator = get_file_byte_chunks(f)
        metadata = (
            ('key-hash-id', hex_dig),
            ('key-chunk-size', str(CHUNK_SIZE))
        )
        response = self.stub.upload_chunk_stream(chunks_generator, metadata=metadata)
        
    def download(self, f_name):
        hash_object = hashlib.sha1(f_name.encode())
        hex_dig = hash_object.hexdigest()
        response = self.stub.download_chunk_stream(chunk_pb2.Request(hash_id=hex_dig))
        # print("Successfully downloaded file with hash_id: ", hash_id)
        # return response