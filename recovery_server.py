from concurrent import futures
import threading
import grpc
import recovery_pb2
import recovery_pb2_grpc
import time
from collections import OrderedDict
import sys

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
hole_dictionary = OrderedDict()
hole_stack = []
global whole_mesh_dictionary
whole_mesh_dictionary = {}
port = "8888"

def findEdgeNode2(meshMap):

    """
    edge_ips = findEdgeNode2(whole_mesh_dictionary)
    if len(edge_ips) :
        edge_ip = edge_ips[0]
    """
    
    edge_coords_ips = []
    top_left = (sys.maxsize,sys.maxsize)
    top_right = (-sys.maxsize,sys.maxsize)
    bottom_left = (sys.maxsize,-sys.maxsize)
    bottom_right = (-sys.maxsize,-sys.maxsize)

    for x,y in meshMap:

        if x <= top_left[0] and y <= top_left[1]:
            top_left[0] = x
            top_left[1] = y
        
        if x >= top_right[0] and y <= top_right[1]:
            top_right[0] = x
            top_right[1] = y
        
        if x <= bottom_left[0] and y >= bottom_left[1]:
            bottom_left[0] = x
            bottom_left[1] = y
        
        if x >= bottom_right[0] and y >= bottom_right[1]:
            bottom_right[0] = x
            bottom_right[1] = y
    
    if abs(top_left[0]) != sys.maxsize and (top_left[0] != 0 and top_left[1] != 0):
        if top_left in meshMap:
            edge_coords_ips.append(top_left)
    
    if abs(top_right[0]) != sys.maxsize:
        if top_right in meshMap and top_left!=top_right:
            edge_coords_ips.append(top_right)

    if abs(bottom_left[0]) != sys.maxsize:
        if bottom_left in meshMap and top_left!=bottom_left and top_right!=bottom_left:
            edge_coords_ips.append(bottom_left)
    
    if abs(bottom_right[0]) != sys.maxsize:
        if bottom_right in meshMap and top_left!=bottom_right and top_right!=bottom_right and bottom_left!=bottom_right:
            edge_coords_ips.append(bottom_right)
        
    return edge_coords_ips



def findEdgeNode(meshMap):

    # print("meshMap",meshMap)

    xlist = set()
    ylist = set()
    for coordinate in meshMap:
        coordinateTuple = coordinate
        xlist.add(coordinateTuple[0])
        ylist.add(coordinateTuple[1])

    try :
        minx = min(xlist)
        miny = min(ylist)
        maxx = max(xlist)
        maxy = max(ylist)

        if 0 != minx or 0 != miny:
            curr = (minx,maxy)
            if curr in meshMap:
                return meshMap[curr]
        
        if 0 != minx or 0 != maxy:
            curr = (minx,maxy)
            if curr in meshMap:
                return meshMap[curr]
        
        if 0 != maxx or 0 != miny:
            curr = (minx,maxy)
            if curr in meshMap:
                return meshMap[curr]
        
        if 0 != maxx or 0 != maxy:
            curr = (minx,maxy)
            if curr in meshMap:
                return meshMap[curr]
    except:
        return ""

    return ""

def getMesh():
    global whole_mesh_dictionary
    while True:
        # we have to change this to any random ip from the list
        try:
            ip = "10.0.0.19"
            recovery_channel = grpc.insecure_channel(ip + ":" + str(port))
            recovery_stub = recovery_pb2_grpc.RecoveryStub(recovery_channel)
            response = recovery_stub.sendWholeMesh(recovery_pb2.SendWholeMeshRequest())
            whole_mesh_dictionary = eval(response.wholemesh)
            # print("whole_mesh_dictionary",eval(response.wholemesh))
            recovery_channel.close()
        except:
            continue
        time.sleep(5)
            

def startRecoveryThread():
    print("Inside recovery thread",hole_dictionary)
    global whole_mesh_dictionary
    while True:
        # print("Recovery",hole_dictionary)
        if len(hole_dictionary) >=3:
            edge_ip = findEdgeNode(whole_mesh_dictionary)
            if edge_ip:
                keys_hole_dictionary = list(d.hole_dictionary())
                pos,neighbors = keys_hole_dictionary[-1]
                hole_dictionary.pop(pos)
                recovery_channel = grpc.insecure_channel(edge_ip + ":" + str(port))
                recovery_stub = recovery_pb2_grpc.RecoveryStub(recovery_channel)
                response = recovery_stub.startRecovery(recovery_pb2.StartRecoveryRequest(pos=str(pos),neighbors=str(neighbors)))
        time.sleep(5)


class RecoveryServer(recovery_pb2_grpc.RecoveryServicer):

    def __init__(self):
        print('Recovery server initialization')

    def sendHoleInfo(self, request, context):
        print("inside hole info method")
        pos = eval(request.pos)
        neighbors = eval(request.neighbors)
        if pos not in hole_dictionary:
            hole_dictionary[pos] = neighbors
        
        print(hole_dictionary)

        return recovery_pb2.SendHoleInfoReply()
            
        


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recovery_pb2_grpc.add_RecoveryServicer_to_server(RecoveryServer(), server)
    server.add_insecure_port('[::]:8888')
    server.start()
    print("Server starting...")

    hole_detection_thread = threading.Thread(target=getMesh)
    hole_detection_thread.start()

    start_recovery_thread = threading.Thread(target=startRecoveryThread)
    start_recovery_thread.start()

    server.wait_for_termination()