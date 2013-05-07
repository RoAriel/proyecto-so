'''
Created on 29/04/2013

@author: Di Meglio
'''

import random
import queues as q


class Scheduler():
    
    def __init__(self,policy):
        self.policy=policy
        
    def get(self):
        return self.policy.get()
    
    def add(self,process):
        self.policy.add(process)




class Policy():
    
    def add(self,process):
        pass
    
    def get(self):
        pass
    
    def isEmpty(self):
        pass


class FCFS(Policy):
    
    def __init__(self):
        self.processes=q.Queue()
    
    
    def add(self,process):
        self.processes.add(process)
        
    def get(self):
        return self.processes.get()
        
        
    def isEmpty(self):
        return self.processes.isEmpty()
    

class SJF(Policy):
    
    def __init__(self):
        self.processes=q.PriorityQueue(lambda pa,pb: pa.priority-pb.priority)
    
    def add(self,process):
        self.processes.add(process)
                
    def get(self):
        return self.processes.get()
        
    def isEmpty(self):
        return self.processes.isEmpty()    
    


class RoundRobin(Policy):
    
    def __init__(self,queue):
        self.processes=queue
        self.quamtum=random(5,20)
    
    def add(self,process):
        self.processes.add(process)
    
    def get(self):
        self.processes.get()
        
    def isEmpty(self):
        return self.processes.isEmpty()
    
    



class Process():
    
    def __init__(self,pid,priority):
        self.pid=pid
        self.priority=priority


#prueba de pq
pa=Process(1,1)
pb=Process(2,5)
pc=Process(3,3)
pd=Process(3,9)
pe=Process(3,3)

s=SJF()
s.add(pa)
s.add(pb)
s.add(pc)
s.add(pd)
s.add(pe)

while not s.isEmpty():
    print s.get().priority

    

