import grpc
import storage_pb2
import storage_pb2_grpc
import threading
import io
import hashlib
import math
import sys

CHUNK_SIZE = 1024 * 1024 * 3  # 4MB
NO_OF_CHUNKS = 0

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

        # data_size = len(f.read())
        data_size = 44740
        print("data_size==", data_size)
        no_of_chunks = math.ceil(data_size / CHUNK_SIZE)
        chunks_generator = get_file_byte_chunks(f)
        metadata = (
            ('key-hash-id', hex_dig),
            ('key-chunk-size', str(CHUNK_SIZE)),
            ('key-number-of-chunks', str(no_of_chunks))
        )
        response = self.stub.upload_chunk_stream(chunks_generator, metadata=metadata)
    
    def sendMessage(self, message, messageId):
        print("Inside Client Method - send")
        # messageBytes = bytearray(message,'utf-8')
        messageBytes = str.encode(message)
        hash_object = hashlib.sha1(messageId.encode())
        hex_dig = hash_object.hexdigest()
        print(hex_dig)

        # data_size = len(f.read())
        data_size = sys.getsizeof(messageBytes)
        print("data_size==", data_size)
        # no_of_chunks = math.ceil(data_size / CHUNK_SIZE)
        message_bytes = storage_pb2.ChunkRequest(chunk=messageBytes)
        
        metadata = (
            ('key-hash-id', hex_dig),
            ('key-chunk-size', str(data_size))
        )
        response = self.stub.upload_single_chunk(message_bytes, metadata=metadata)
        
    def download(self, f_name):
        hash_object = hashlib.sha1(f_name.encode())
        hex_dig = hash_object.hexdigest()
        response = self.stub.download_chunk_stream(storage_pb2.HashIdRequest(hash_id=hex_dig))
        with open("./"+f_name,'wb') as f:
            for c in response:
                f.write(c.chunk)
    
    def getMessage(self, messageId):
        hash_object = hashlib.sha1(messageId.encode())
        hex_dig = hash_object.hexdigest()
        response = self.stub.download_chunk_stream(storage_pb2.HashIdRequest(hash_id=hex_dig))
        print("response====",response)
        message_bytes = bytearray()
        for c in response:
            message_bytes.extend(c.chunk)
        message = message_bytes.decode()
        return message