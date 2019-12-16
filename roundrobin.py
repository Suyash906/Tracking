import os;
import pickle;
ips = ["localhost:9999"]
def readIndex():
    try:
        fName = os.getcwd()+"/sharedIndex.pkl"
        with open(fName,'rb') as fp:
            return int(pickle.load(fp))
    except IOError:
        sharedIndex = 0
        fp = open(os.getcwd()+"/sharedIndex.pkl","wb")
        pickle.dump(sharedIndex, fp)
        return sharedIndex

def writeIndex():
    try:
        sharedIndex = readIndex()
        sharedIndex = int(sharedIndex) + 1
        if(sharedIndex >= len(ips)):
            sharedIndex = 0
        fp = open(os.getcwd()+"/sharedIndex.pkl","wb")
        pickle.dump(sharedIndex, fp)
        return 1
    except IOError:
        return 0


def getIpAddress():
    ip = readIndex();
    writeIndex();
    return ips[ip]

print(getIpAddress())