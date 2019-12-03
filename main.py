import os
from fileObject import fileObject
import pickle
import time
# constant chunk size
chunksize = 1000

def readSharedDictionary():
    try:
        fName = os.getcwd()+"/shared.pkl"
        with open(fName,'rb') as fp:
            return pickle.load(fp)
    except IOError:
        shared = {}
        fp = open(os.getcwd()+"/shared.pkl","wb")
        pickle.dump(shared, fp)
        return shared

def writeToSharedDictionary(f):
    try:
        shared = readSharedDictionary()
        shared[f.filename] = f
        fp = open(os.getcwd()+"/shared.pkl","wb")
        pickle.dump(shared, fp)
        return 1
    except IOError:
        return 0

def split(source):
    # print("testing")
    #create Dictionary Object
    f = fileObject(source)
    prefix, fn = os.path.split(source)
    fn, ext = os.path.splitext(fn)
    f.set_filename(fn)
    f.set_extension(ext)
    
    
    # Make a destination folder if it doesn't exist yet
    dest_folder = os.getcwd()+"/chunks/"+fn+"/"
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    else:
        # Otherwise clean out all files in the destination folder
        for file in os.listdir(dest_folder):
            os.remove(os.path.join(dest_folder, file))

    partnum = 0
    f.set_size(os.path.getsize(source))
    
    
    

    # Open the source file in binary mode
    input_file = open(source, 'rb')
 
    while True:
        # Read a portion of the input file
        chunk = input_file.read(chunksize)
        
        # End the loop if we have hit EOF
        if not chunk:
            break
 
        # Increment partnum
        partnum += 1
        
        # Create a new file name 
        filename = os.path.join(dest_folder, 'part_'+str(partnum))
        print("filename==",filename,fn)
        f.add_part(filename)

        # Create a destination file
        dest_file = open(filename, 'wb')
 
        # Write to this portion of the destination file
        dest_file.write(chunk)
 
        # Explicitly close 
        dest_file.close()
     
    # Explicitly close
    input_file.close()

    # write to a common file
    writeToSharedDictionary(f)
    
    #sendRequest(f)
    
    # Return the number of files created by the split
    return f.filename
 
 
def join(requested_file):
    
    shared = readSharedDictionary()
    try:
        f = shared[requested_file]    
    except KeyError:
        print("File Not Found")
        return

    # Get a list of the file parts
    parts = f.get_parts()

    # Create a new destination file
    output_file = open("output/" + requested_file + f.get_extension(), 'wb')
     
    # Sort them by name (remember that the order num is part of the file name)
    parts.sort()
 
    # Go through each portion one by one
    for file in parts:
         
        # Assemble the full path to the file
        #path = os.path.join(, file)
         
        # Open the part
        input_file = open(file, 'rb')
         
        while True:
            # Read all bytes of the part
            bytes = input_file.read(chunksize)
            # Break out of loop if we are at end of file
            if not bytes:
                break
            
            # Write the bytes to the output file
            output_file.write(bytes)
             
        # Close the input file
        input_file.close()
         
    # Close the output file
    output_file.close()


# parts = split("sample.txt")
# print("File Split into " , parts)
# time.sleep(5)
# join("sample")
