'''
Created on 17/06/2013

@author: fernando
'''

class A():
    
    def __init__(self,i):
        self.i=i

import Queue as q

q=q.PriorityQueue(100)
a=A(1)
q.put(a,a.i)
b=A(2)
q.put(b,b.i)
c=A(3)
q.put(c,c.i)

print q.get().i



print (1,2)