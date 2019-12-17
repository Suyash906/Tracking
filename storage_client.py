import grpc
import storage_pb2
import storage_pb2_grpc
import io
import hashlib
import math
import sys
import os
import funcy
import uuid

CHUNK_SIZE = 1024 * 1024 * 3  # 3MB
NO_OF_CHUNKS = 0

def get_file_byte_chunks(f, size_of_chunk):
    # while True:
    #     piece = f.read(CHUNK_SIZE)
    #     if len(piece) == 0:
    #         return
    #     yield storage_pb2.ChunkRequest(chunk=piece)
    # print("size_of_chunk ==",size_of_chunk)
    # print("no_of_chunks ==",no_of_chunks)
    # for i in range(no_of_chunks):
    #     print("(size_of_chunk*i)==", (size_of_chunk*i))
    #     print("(i+1)*size_of_chunk-1==", (i+1)*size_of_chunk-1)
    #     print("f[(size_of_chunk*i):(i+1)*size_of_chunk-1]=====", f[(size_of_chunk*i):(i+1)*size_of_chunk-1])
    #     yield storage_pb2.ChunkRequest(chunk=f[(size_of_chunk*i):(i+1)*size_of_chunk-1])
    chunk_list = list(funcy.chunks(size_of_chunk, f))

    for chunk in chunk_list:
        print("chunk==",chunk)
        yield storage_pb2.ChunkRequest(chunk=chunk)

class Client:
    def __init__(self, address):
            channel = grpc.insecure_channel(address)
            self.stub = storage_pb2_grpc.FileServerStub(channel)
    
    def upload(self, f, f_name, size):
        print("Inside here")
        hash_object = hashlib.sha1(f_name.encode())
        hex_dig = hash_object.hexdigest()
        print("hex_dig==",hex_dig)

        #data_size = len(f.read())
        # data_size = os.path.getsize("/Users/wamiqueansari/Downloads/tweet-unlike-icon.png")
        # data_size = 9658
        fBytes = str.encode(f)
        print("data_size==", size)
        no_of_chunks = math.ceil(size / CHUNK_SIZE)
        size_of_chunk = math.ceil(size / no_of_chunks)
        chunks_generator = get_file_byte_chunks(fBytes, size_of_chunk)
        print("testtttttttt")
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
        print("hex_dig==",hex_dig)

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
        try:
            response = self.stub.download_chunk_stream(storage_pb2.HashIdRequest(hash_id=hex_dig))
            print('==============response==============')
            print(response)
            # with open("./"+f_name,'wb') as f:
            #     for c in response:
            #         f.write(c.chunk)
            file_bytes = bytearray()
            for c in response:
                file_bytes.extend(c.chunk)
            file = file_bytes.decode()
            return file
        except Exception as e:
            # print("there was an error in download file")
            return None
    
    def getMessage(self, messageId):
        try:
            hash_object = hashlib.sha1(messageId.encode())
            hex_dig = hash_object.hexdigest()
            response = self.stub.download_chunk_stream(storage_pb2.HashIdRequest(hash_id=hex_dig))
            print("response====",response)
            message_bytes = bytearray()
            for c in response:
                message_bytes.extend(c.chunk)
            message = message_bytes.decode()
            return message
        except Exception as e:
            # print("there was an error in get message")
            return None