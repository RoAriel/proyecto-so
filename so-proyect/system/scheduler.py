'''
Created on 29/04/2013

@author: Di Meglio
'''

import random
import queues as q
import clock
from interruptions  import Interruption 
import interruptions as i

class Scheduler():
    
    def __init__(self,policy):
        self.policy=policy
        
    def get(self):
        return self.policy.get()
    
    def add(self,process):
        self.policy.add(process)

    def getTimer(self):
        return self.policy.getTimer()


class Policy():
    
    def add(self,process):
        pass
    
    def get(self):
        pass
    
    def isEmpty(self):
        pass
    
    def getTimer(self):
        return clock.Timer()


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
    
    def __init__(self,isExpropriation):
        self.running=None
        self.isExpropriation=isExpropriation
        self.processes=q.PriorityQueue(lambda pa,pb: pa.priority-pb.priority)
    
    def add(self,process):
        #si no es expropiativo simplemente lo agrega a la cola de espera
        #caso contrario le indica a la managerInterruption cual es el proceso
        #que va a expropiar y lanza la interrupcino de expropiacion
        if(not self.isExpropriation):
            self.processes.add(process)
        else:
            i.ManagerInterruptions.pcbExpropiation=process
            i.ManagerInterruptions.throwInterruption(Interruption.expropiation)
            
    def doOld(self):
        processes=q.PriorityQueue(lambda pa,pb: pa.priority-pb.priority)
        while not self.isEmpty():
            p=processes.get()
            p.priority+=2
            processes.add(p)
        
        self.processes=processes
            
            
                
    def get(self):
        running=self.processes.get()
        self.doOld()
        return running
        
    def isEmpty(self):
        return self.processes.isEmpty()    
    


class RoundRobin(Policy):
    
    def __init__(self,isPriority):
        
        self.quamtum=random.randrange(5, 20)
        if(isPriority):
            self.processes=q.Queue()
        else:
            self.processes=q.PriorityQueue(lambda pa,pb: pa.priority-pb.priority)
    
    def add(self,process):
        self.processes.add(process)
    
    def get(self):
        self.processes.get()
        
    def isEmpty(self):
        return self.processes.isEmpty()
    
    def getTimer(self):
        return clock.TimerQuantum()



class Process():
    
    def __init__(self,pid,priority):
        self.pid=pid
        self.priority=priority






    

