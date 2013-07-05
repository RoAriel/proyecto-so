'''
Created on 06/05/2013

@author: usuario
'''
import Queue

class PQueueToPcb(Queue.PriorityQueue):
    
    def put(self,pcb):
        Queue.PriorityQueue.put(self,pcb,pcb.priority)



