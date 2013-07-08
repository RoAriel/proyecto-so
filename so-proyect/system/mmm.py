'''
Created on 08/07/2013

@author: CABJ
'''
import Queue

q=Queue.PriorityQueue()

q.put((1,'a'))
q.put((3,'b'))
q.put((2,'c'))

while not q.empty():
    print q.get()