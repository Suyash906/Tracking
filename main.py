import os
from fileObject import fileObject
import time
# constant chunk size
chunksize = 10000
def split(source, dest_folder):
    f = fileObject(source)
    # Make a destination folder if it doesn't exist yet
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    else:
        # Otherwise clean out all files in the destination folder
        for file in os.listdir(dest_folder):
            os.remove(os.path.join(dest_folder, file))

    partnum = 0
    f.set_size(os.path.getsize(source))
    
    #create Dictionary Object
    fn, file_extension = os.path.splitext(source)
    f.set_filename(fn)
    f.set_extension(file_extension)
    
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
        filename = os.path.join(dest_folder, 'part'+str(partnum))
        f.add_part(filename)

        # Create a destination file
        dest_file = open(filename, 'wb')
 
        # Write to this portion of the destination file
        dest_file.write(chunk)
 
        # Explicitly close 
        dest_file.close()
     
    # Explicitly close
    input_file.close()
    print(f)
    # Return the number of files created by the split
    return partnum
 
 
def join(source_dir, dest_file):
    # Create a new destination file
    output_file = open(dest_file, 'wb')
     
    # Get a list of the file parts
    parts = os.listdir(source_dir)
     
    # Sort them by name (remember that the order num is part of the file name)
    parts.sort()
 
    # Go through each portion one by one
    for file in parts:
         
        # Assemble the full path to the file
        path = os.path.join(source_dir, file)
         
        # Open the part
        input_file = open(path, 'rb')
         
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


split("sample.txt", "chunks")
#join("chunks", "tttt")