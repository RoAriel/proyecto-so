'''
Created on 29/04/2013

@author: Di Meglio
'''

import random

class Scheduler():
    
    def __init__(self,policy):
        self.policy=policy
        
    def get(self):
        return self.policy.get()
    
    def add(self,process):
        self.policy.add(process)




class policy():
    
    def add(self,process):
        pass
    
    def get(self):
        pass
    
    def isEmpty(self):
        pass


class FCFS(policy):
    
    def __init__(self):
        self.processes=[]
    
    
    def add(self,process):
        self.processes.append(process)
        
    def get(self):
        process=self.processes[0]
        self.processes.remove(process)
        return process
        
    def isEmpty(self):
        return len(self.processes)==0
    


class RoundRobin(FCFS):
    
    def __init__(self):
        self.processes=[]
        self.quamtum=random(5,20)
    
    
    def add(self,process):
        self.add(process)   
                
        
    def get(self):
        process=self.get()
        if(not process.time-self.quamtum<=0):
            self.add(process)
        return process
        
    def isEmpty(self):
        return len(self.processes)==0



class Process():
    
    def __init__(self,name,time):
        self.name=name
        self.time=time
    
queue =FCFS()
queue.add(Process(1,1))
queue.add(Process(2,2))
queue.add(Process(3,3))
queue.add(Process(4,4))
queue.add(Process(5,5))


while(not queue.isEmpty()):
    p= queue.get()

    print p.name
        