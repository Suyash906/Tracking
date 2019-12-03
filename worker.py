from threading import Thread
from queue import Queue
#import Document
import time
import os


def handleCreateFileRequest(q):
	while True:
		print("Getting an element from Request queue: ")

		t = q.get()
		print(t[1],"print tee")

		if t[1] == "write":
			cwd = os.getcwd()
			statinfo = os.stat(cwd + "/uploads/"+t[0])
			print(statinfo.st_size) #it shows in bytes
			if statinfo.st_size > 500:
				chunk_queue.put(t)
			else: forward_queue.put(t)
		q.task_done()

def handleChunkFileRequest(q):
	while True:
		print("Getting an element from Chunk queue: ")
		print(q.get())
		q.task_done()

def handleForwardFileRequest(q):
	while True:
		print("Getting an element from Forward queue: ")
		print(q.get())
		q.task_done()

def testing():
	print("=====Request Queue=====")
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 1 in queue")
	request_queue.put((1,"write"))
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 2 in queue")
	request_queue.put((2,"update"))
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 3 in queue")
	request_queue.put((3,"read"))

	

	print("=====Chunk Queue=====")
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 1 in queue")
	chunk_queue.put(1)
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 2 in queue")
	chunk_queue.put(2)
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 3 in queue")
	chunk_queue.put(3)

	

	print("=====Forward Queue=====")
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 1 in queue")
	forward_queue.put(1)
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 2 in queue")
	forward_queue.put(2)
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 3 in queue")
	forward_queue.put(3)

	request_worker.join()
	chunk_worker.join()
	forward_worker.join()

 
def split(source, dest_folder, write_size):
    # Make a destination folder if it doesn't exist yet
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    else:
        # Otherwise clean out all files in the destination folder
        for file in os.listdir(dest_folder):
            os.remove(os.path.join(dest_folder, file))
 
    partnum = 0
    
    # b = os.path.getsize(source)
    # chunksize = 

    # Open the source file in binary mode
    input_file = open(source, 'rb')
 
    while True:
        # Read a portion of the input file
        chunk = input_file.read(write_size)
 
        # End the loop if we have hit EOF
        if not chunk:
            break
 
        # Increment partnum
        partnum += 1
 
        # Create a new file name
        filename = os.path.join(dest_folder, 'part'+str(partnum))
        print(filename)
        # Create a destination file
        dest_file = open(filename, 'wb')
 
        # Write to this portion of the destination file
        dest_file.write(chunk)
 
        # Explicitly close 
        dest_file.close()
     
    # Explicitly close
    input_file.close()
     
    # Return the number of files created by the split
    return partnum

def enqueue_request_queue(filename, handle_type):
	 request_queue.put((filename,handle_type))

request_queue = Queue(maxsize=0)
request_worker = Thread(target=handleCreateFileRequest, args=(request_queue,))
request_worker.start()

chunk_queue = Queue(maxsize=0)
chunk_worker = Thread(target=handleChunkFileRequest, args=(chunk_queue,))
chunk_worker.start()

forward_queue = Queue(maxsize=0)
forward_worker = Thread(target=handleForwardFileRequest, args=(forward_queue,))
forward_worker.start()

# testing()