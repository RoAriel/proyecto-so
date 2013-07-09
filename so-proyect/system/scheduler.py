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
    def addAsReady(self,pcb):
        self.policy.addAsReady(pcb)
    
    def add(self,pcb,cpu):
        if((cpu.pcb is None) & self.isEmpty()):
            cpu.pcb=pcb
        else:
            self.policy.add(pcb,cpu)
        
        
    def isEmpty(self):
        return self.policy.isEmpty()

    def getTimer(self):
        return self.policy.getTimer()

    def getQueue(self):
        return self.policy.getQueue()
    
    def kill(self,pcb):
        self.policy.kill(pcb)
        
    def showReedyProcess(self):
        self.policy.showReedyProcess()

class Policy():
    
    def __init__(self):
        self.processes=q.Queue()
    
    def isEmpty(self):
        return self.processes.empty()
    
    def getTimer(self):
        return clock.Timer()
    
    """Si el proceso esta en la cola de lista lo saca"""    
    def kill(self,pcb):
        newQueue=q.Queue()
        while not self.processes.empty():
            x=self.processes.get()
            if(not x == pcb):
                newQueue.put(x)
        self.processes=newQueue


    def getQueue(self):
        return q.Queue()
    
    def showReedyProcess(self):
        newQueue=q.Queue()
        while not self.processes.empty():
            x=self.processes.get()
            print x.pid
            newQueue.put(x)
        self.processes=newQueue

class FCFS(Policy):
    
    def __init__(self):
        Policy.__init__(self)
    
    
    def add(self,pcb,cpu):
        self.processes.put(pcb)
        
    def get(self):
        return self.processes.get()
        

    

class SJF(Policy):
    
    def __init__(self,isExpropriation):
        self.isExpropriation=isExpropriation
        self.processes=qp.PQueueToPcb()
    
    def add(self,pcb,cpu):
        #si no es expropiativo simplemente lo agrega a la cola de espera
        #caso contrario le indica a la managerInterruption cual es el proceso
        #que va a expropiar y lanza la interrupcino de expropiacion
        
        #Agrega la variable priority al pcb en tiempo de ejecucion
        pcb.priority=random.randrange(1,150)
        
        if(self.isExpropriation):
            if(cpu.pcb.priority > pcb.priority):
                self.processes.put(pcb)
            else:
                i.ManagerInterruptions.throwInterruption(Interruption.expropiation,GloabalContext(pcb))
        else:
            self.processes.put(pcb)
    
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
    """Si el proceso esta en la cola de lista lo saca"""   
    def kill(self,pcb):
        newQueue=qp.PQueueToPcb()
        while self.processes.empty():
            x=self.processes.get()
            if(not x == pcb):
                newQueue.put(x)
        self.processes=newQueue
    
    def showReedyProcess(self):
        newQueue=qp.PQueueToPcb()
        while self.processes.empty():
            x=self.processes.get()
            print x.pid
            newQueue.put(x)
        self.processes=newQueue
        

class RoundRobin(Policy):
    
    def __init__(self,isPriority,quantum):
        Policy.__init__(self)
        self.isPriority=isPriority
        self.quamtum=quantum
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
    
    """Envejecimiento de procesos"""       
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

    """Si el proceso esta en la cola de lista lo saca"""
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

    def showReedyProcess(self):
        if(self.isPriority):
            newQueue=qp.PQueueToPcb()
            while self.processes.empty():
                x=self.processes.get()
                print x.pid
                newQueue.put(x)
            self.processes=newQueue
        else:
            Policy.showReedyProcess(self)
    

