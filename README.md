
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
  python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/example.proto
```
