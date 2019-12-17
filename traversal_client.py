import grpc
import traversal_pb2
import traversal_pb2_grpc
import io
import hashlib
import math
import sys
import os
import funcy
import uuid

CHUNK_SIZE = 1024 * 1024 * 3  # 3MB
NO_OF_CHUNKS = 0

class TraversalClient:
    def __init__(self, address, ip):
            self.ip = ip
            channel = grpc.insecure_channel(address)
            self.stub = traversal_pb2_grpc.TraversalStub(channel)
    
    def download(self, f_name):
        hash_object = hashlib.sha1(f_name.encode())
        hex_dig = hash_object.hexdigest()
        print("hexdigit: {}".format(hex_dig))
        # response = self.stub.download_chunk_stream(storage_pb2.HashIdRequest(hash_id=hex_dig))
        request_id = uuid.uuid1()
        visited_ip = []
        response = self.stub.ReceiveData(
            traversal_pb2.ReceiveDataRequest(
                                hash_id=hex_dig,
                                request_id=str(request_id),
                                stack="",
                                visited=str(visited_ip),
                                requesting_node_ip=self.ip))
        print('==============response==============')
        print(response)
        # with open("./"+f_name,'wb') as f:
        #     for c in response:
        #         f.write(c.chunk)
        # file_bytes = bytearray()
        # for c in response:
        #     file_bytes.extend(c.chunk)
        file = response.file_bytes.decode()
        return file