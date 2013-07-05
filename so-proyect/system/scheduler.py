'''
Created on 29/04/2013

@author: Di Meglio
'''

import random
import queuePCB as qp
import Queue as q
import clock
from interruptions  import Interruption 
import interruptions as i
import random
from interruptions import GloabalContext

class Scheduler():
    
    def __init__(self,policy):
        self.policy=policy
        
    def get(self):
        if(self.policy.isEmpty()):
            return None
        return self.policy.get()
    
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
    
    def __init__(self):
        self.processes=q.Queue()
    
    def add(self,process,cpu):
        pass
    
    def addAsReady(self):
        pass
    
    def get(self):
        pass
    
    def isEmpty(self):
        return self.processes.empty()
    
    def getTimer(self):
        return clock.Timer()


class FCFS(Policy):
    
    def __init__(self):
        Policy.__init__(self)
    
    
    def add(self,process,cpu):
        self.processes.put(process)
        
    def get(self):
        return self.processes.get()
        

    

class SJF(Policy):
    
    def __init__(self,isExpropriation):
        self.isExpropriation=isExpropriation
        self.processes=qp.PQueueToPcb()
    
    def add(self,process,cpu):
        #si no es expropiativo simplemente lo agrega a la cola de espera
        #caso contrario le indica a la managerInterruption cual es el proceso
        #que va a expropiar y lanza la interrupcino de expropiacion
        
        #Agrega la variable priority al pcb en tiempo de ejecucion
        process.priority=random.randrange(1,150)
        
        if(self.isExpropriation):
            if(cpu.pcb.priority > process.priority):
                self.processes.put(process)
            else:
                i.ManagerInterruptions.throwInterruption(Interruption.expropiation,GloabalContext(process))
        else:
            self.processes.put(process)
    
    def addAsReady(self,process):
        self.processes.put(process)      
            
    def doOld(self):
        processes=qp.PQueueToPcb()
        while not self.isEmpty():
            p=self.processes.get()
            p.priority+=2
            processes.put(p)
        
        self.processes=processes
            
            
                
    def get(self):
        running=self.processes.get()
        self.doOld()
        return running
            
    


class RoundRobin(Policy):
    
    def __init__(self,isPriority):
        Policy.__init__(self)
        self.quamtum=random.randrange(1, 5)
        if(isPriority):
            self.processes=qp.PQueueToPcb()
    
    def add(self,process,cpu):
        self.processes.put(process)
    
    def get(self):
        return self.processes.get()
        
    
    def getTimer(self):
        return clock.TimerQuantum(3)





    

