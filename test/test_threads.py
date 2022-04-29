import threading
import os
# global variable x
x = 0

# def increment():
# 	"""
# 	function to increment global variable x
# 	"""
# 	global x
# 	x += 1

# def thread_task(lock):
# 	"""
# 	task for thread
# 	calls increment function 100000 times.
# 	"""
# 	for _ in range(100000):
# 		lock.acquire()
# 		increment()
# 		lock.release()

def task1(lock):
    for i in range(10):
        pass        
    print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 1: {}".format(os.getpid()))
    
   

def task2(lock):
    print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 2: {}".format(os.getpid()))


def main_task():
	global x
	# setting global variable x as 0
	x = 0
    
	# creating a lock
	lock = threading.Lock()

	# creating threads
	t1 = threading.Thread(target=task1, args=(lock,), name='t1')
	t2 = threading.Thread(target=task2, args=(lock,), name='t2')

	# start threads
	t1.start()
	t2.start()

	# wait until threads finish their job
	t1.join()
	t2.join()

if __name__ == "__main__":
	
		main_task()
