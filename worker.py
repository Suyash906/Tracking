from threading import Thread
from queue import Queue
#import Document
import time

def handleCreateFileRequest(q):
	while True:
		print("Getting an element from Request queue: ")
		print(q.get())
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
	request_queue.put(1)
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 2 in queue")
	request_queue.put(2)
	print("Sleeping for 5 secs")
	time.sleep(5)
	print("Putting 3 in queue")
	request_queue.put(3)

	

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

request_queue = Queue(maxsize=0)
request_worker = Thread(target=handleCreateFileRequest, args=(request_queue,))
request_worker.start()

chunk_queue = Queue(maxsize=0)
chunk_worker = Thread(target=handleChunkFileRequest, args=(chunk_queue,))
chunk_worker.start()

forward_queue = Queue(maxsize=0)
forward_worker = Thread(target=handleForwardFileRequest, args=(forward_queue,))
forward_worker.start()

testing()