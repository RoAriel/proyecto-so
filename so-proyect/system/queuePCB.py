'''
Created on 06/05/2013

@author: usuario
'''
import Queue

"""Cola con prioridad para procesos"""
class PQueueToPcb(Queue.PriorityQueue):
    
    def put(self,pcb):
        Queue.PriorityQueue.put(self,(pcb.priority,pcb))

    def get(self):
        return Queue.PriorityQueue.get(self)[0]

