'''
Created on 29/04/2013

@author: Di Meglio
'''

import random
import queues as q
import clock
from interruptions  import Interruption 
import interruptions as i
import random
from threading import  Semaphore

class Scheduler():
    
    def __init__(self,policy):
        self.policy=policy
        self.semaphore = Semaphore(1)
        
    def get(self):
        if(self.policy.isEmpty()):
            return None
        process=self.policy.get()
        return process
    
# agrega al proceso directamente como listo    
    def addAsReady(self,process):
        self.policy.addAsReady(process)
    
    def add(self,process,cpu):
        self.policy.add(process,cpu)
        
    def isEmpty(self):
        return self.policy.isEmpty()

    def getTimer(self):
        return self.policy.getTimer()


class Policy():
    
    def add(self,process,cpu):
        pass
    
    def addAsReady(self):
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
    
    
    def add(self,process,cpu):
        self.processes.add(process)
        
    def get(self):
        return self.processes.get()
        
        
    def isEmpty(self):
        return self.processes.isEmpty()
    

class SJF(Policy):
    
    def __init__(self,isExpropriation):
        self.isExpropriation=isExpropriation
        self.processes=q.PriorityQueue(lambda pa,pb: pa.priority-pb.priority)
    
    def add(self,process,cpu):
        #si no es expropiativo simplemente lo agrega a la cola de espera
        #caso contrario le indica a la managerInterruption cual es el proceso
        #que va a expropiar y lanza la interrupcino de expropiacion
        if(self.isExpropriation):
            if(cpu.pcb.priority > process.priority):
                self.processes.add(process)
            else:
                i.ManagerInterruptions.pcbExpropiation=process
                i.ManagerInterruptions.throwInterruption(Interruption.expropiation)
        else:
            self.processes.add(process)
    
    def addAsReady(self,process):
        self.processes.add(process)      
            
    def doOld(self):
        processes=q.PriorityQueue(lambda pa,pb: pa.priority-pb.priority)
        while not self.isEmpty():
            p=self.processes.get()
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
        
        self.quamtum=random.randrange(1, 5)
        if(isPriority):
            self.processes=q.PriorityQueue(lambda pa,pb: pa.priority-pb.priority)
        else:
            self.processes=q.Queue()
    
    def add(self,process,cpu):
        self.processes.add(process)
    
    def get(self):
        return self.processes.get()
        
    def isEmpty(self):
        return self.processes.isEmpty()
    
    def getTimer(self):
        return clock.TimerQuantum(3)






    

