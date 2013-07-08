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
        if((cpu.pcb is None) & self.isEmpty()):
            cpu.pcb=process
        else:
            self.policy.add(process,cpu)
        
        
    def isEmpty(self):
        return self.policy.isEmpty()

    def getTimer(self):
        return self.policy.getTimer()

    def getQueue(self):
        return self.policy.getQueue()
    
    def kill(self,pcb):
        self.policy.kill(pcb)

class Policy():
    
    def __init__(self):
        self.processes=q.Queue()
    
    def isEmpty(self):
        return self.processes.empty()
    
    def getTimer(self):
        return clock.Timer()
        
    def kill(self,pcb):
        newQueue=q.Queue()
        while not self.processes.empty():
            x=self.processes.get()
            if(not x == pcb):
                newQueue.put(x)
        self.processes=newQueue


    def getQueue(self):
        return q.Queue()

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
            
    def getQueue(self):
        return qp.PQueueToPcb()    
                
    def get(self):
        running=self.processes.get()
        self.doOld()
        return running
        
    def kill(self,pcb):
        newQueue=qp.PQueueToPcb()
        while self.processes.empty():
            x=self.processes.get()
            if(not x == pcb):
                newQueue.put(x)
        self.processes=newQueue
    


class RoundRobin(Policy):
    
    def __init__(self,isPriority):
        Policy.__init__(self)
        self.isPriority=isPriority
        self.quamtum=random.randrange(1, 5)
        if(isPriority):
            self.processes=qp.PQueueToPcb()
    
    def add(self,process,cpu):
        if(self.isPriority):
            process.priority=random.randrange(1,150)
        self.processes.put(process)
    
    def get(self):
        pcb=self.processes.get()
        if(self.isPriority):
            self.doOld()
        return pcb
            
    def doOld(self):
        processes=qp.PQueueToPcb()
        while not self.isEmpty():
            p=self.processes.get()
            p.priority+=2
            processes.put(p)
        self.processes=processes  
    
    def getTimer(self):
        return clock.TimerQuantum(3)

    def getQueue(self):
        if(self.isPriority):
            return qp.PQueueToPcb()
        else:
            return Policy.getQueue(self)

    def kill(self,pcb):
        if(self.isPriority):
            newQueue=qp.PQueueToPcb()
            while self.processes.empty():
                x=self.processes.get()
                if(not x == pcb):
                    newQueue.put(x)
            self.processes=newQueue
        else:
            Policy.kill(self, pcb)


    

