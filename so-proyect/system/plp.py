'''
Created on 17/06/2013

@author: usuario
'''

"""Muy simple version de planificador de largo plazo,solo controla si hay memoria 
   disponible
"""

class PLP():
    
    def __init__(self,memory,scheduler):
        self.memory=memory
        self.queueWait=scheduler.getQueue()
        self.scheduler=scheduler
        memory.plp=self
        
    def allocateMemory(self,pcb):
        if(self.memory.getFreeSpace() >= pcb.size):
            self.memory.allocateMemory(pcb)
            self.scheduler.add(pcb)
        else:
            self.queueWait.add(pcb)
            
    def notify(self,size):
        newQueue=self.scheduler.getQueue()
        flag=True
        while not self.queueWait.empty():
            pcb=self.queueWait.get()
            if(pcb.size<=size & flag):
                self.memory.allocateMemory(pcb)
                self.scheduler.add(pcb)
                flag=False
            else:
                newQueue.put(pcb)
        self.queueWait=newQueue
            
            
                
            