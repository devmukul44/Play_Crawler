import thread
import time

# Define a function for the thread
def print_time(threadName):
      print threadName

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1",) )
   thread.start_new_thread( print_time, ("Thread-2",) )
except:
   print "Error: unable to start thread"

while 1:
   pass
