'''
Created on 17/06/2013

@author: j di meglio
'''

"""Muy simple version de planificador de largo plazo,solo controla si hay memoria 
   disponible o disco(para caso de paginacion)
"""
from processAndProgram import State
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
            pcb.state=State.ready
        else:
            pcb.state=State.wait
            self.queueWait.put(pcb)
    
    """Este metodo se uliliza para cuando la memori logica mata un proceso,
       y notifica llamando a este metodo.Tambien controla que el pcb no halla finalizado
    """        
    def notify(self,size):
        newQueue=self.scheduler.getQueue()
        flag=True
        while not self.queueWait.empty():
            pcb=self.queueWait.get()
            if(pcb.getSize()<=size and flag and pcb.state != State.finished):
                self.memory.allocateMemory(pcb)
                self.scheduler.add(pcb,self.cpu)
                flag=False
            else:
                if(pcb.state != State.finished):
                    newQueue.put(pcb)
        self.queueWait=newQueue
            
            
                
            