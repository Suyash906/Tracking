# CMPE 275(Enterprise Application Development) Project - Middleware Team Repo

## Team Members
1. [Divisha Bera](https://github.com/divishabera)
2. [Suyash Srivastava](https://github.com/Suyash906)
3. [Tosha Kamath](https://github.com/toshakamath)
4. [Vinit Dholakia](https://github.com/vinitdholakia)
5. [Wamique Ansari](https://github.com/wamiquem)

## Introduction
Develop the middleware server in project to act as an interface between the two applications (messaging and dropbox - serving as client) and the Mesh network. The two front end application teams made http requests which were handled by python flask at the middleware server. To serve the request, the middleware made gRPC requests to the Mesh network. The response received from the mesh is sent to the front end application.

The following three areas have been identified for the middleware:

<b>Load Balancing Requests</b>: Implemented classical load balancing by distributing the request in a round robin fashion to the Mesh team. The list of mesh Node IPs was maintained in a list at the middleware end. Any request from the application end was forwarded to one of the mesh nodes by picking up the IP from the list in round robin fashion.

<b>Caching</b>: For read requests, apart from the actual data the mesh nodes was also sending the the node IP where the data resided. This allowed caching of the node IP as value and request ID as key at the middleware end. Thus, the latency of the future request of the same data was reduced.    

<b>Recovery Node Trigger</b>: The middleware team periodically requests the logical mesh grid snapshot as well as the list of failed nodes from the fault tolerance module in the mesh. As soon as the number of holes in network reaches the count 3, then middleware initiates node recovery for the 3 holes in last in first out order. The node with minimum number of connections is selected as the replacement node. The middleware sends request to the fault tolerance module in the Mesh network with the hole and the replacement node. The fault tolerance team processes the recovery of the network.

## Approach  
1. <b>Files request handling by saving it on disk(Branch - oldVersion)</b>- In this approach, the files sent by the client in POST request gets downloaded onto the disk. The file is read from the disk and broken down into chunks which are again saved on the disk. The individual chunks are again read from the disk and send out to the mesh network for storage.
2. <b>Files request handling by passing processing it as stream(Branch - master)</b> - In this approach the file transfer process was done in-memory. The application sent the files in the request in bytes format. The bytes was broken down into chunks of 4MB and passed as a stream to the mesh team. The 4MB chunk size was fixed because, in gRPC the maximum size that could be transferred in a request is 4MB.


## Installation Steps

### Install python virtual env:
```
  1.  python -m pip install virtualenv
  2.  virtualenv venv
  3.  source venv/bin/activate
  4.  python -m pip install --upgrade pip
```

### Package Installation
```
  1. pip install flask
  2. pip install grpcio
  3. pip install grpcio-tools
  4. sudo pip install grpc
```

###  Generate Code
```
  1. python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/storage.proto
  2. python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/traversal.proto
  3. python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/recovery.proto
```


## 
