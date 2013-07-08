'''
Created on 17/06/2013

@author: usuario
'''

"""Muy simple version de planificador de largo plazo,solo controla si hay memoria 
   disponible
"""

class PLP():
    
    def __init__(self,memory,scheduler,cpu):
        self.memory=memory
        self.queueWait=scheduler.getQueue()
        self.scheduler=scheduler
        memory.plp=self
        self.cpu=cpu
        
    def allocateMemory(self,pcb):
        if(self.memory.freeSpaceInMemory(pcb.getSize()) & self.memory.freeSpaceInDisk(pcb.getSize())):
            self.memory.allocateMemory(pcb)
            self.scheduler.add(pcb,self.cpu)
        else:
            self.queueWait.put(pcb)
    
    """Este metodo se uliliza para cuando la memori logica mata un proceso,
       y notifica llamando a este metodo
    """        
    def notify(self,size):
        newQueue=self.scheduler.getQueue()
        flag=True
        while not self.queueWait.empty():
            pcb=self.queueWait.get()
            if(pcb.getSize()<=size & flag):
                self.memory.allocateMemory(pcb)
                self.scheduler.add(pcb)
                flag=False
            else:
                newQueue.put(pcb)
        self.queueWait=newQueue
            
            
                
            