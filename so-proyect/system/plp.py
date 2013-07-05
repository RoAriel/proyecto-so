'''
Created on 17/06/2013

@author: usuario
'''
class PLP():
    
    def __init__(self,memory,queueWait,scheduler):
        self.memory=memory
        self.queueWait=queueWait
        self.scheduler=scheduler
        
    def addPcb(self,pcb):
        if(self.memory.getFreeSpace() >= pcb.size):
            self.memory.allocateMemory(pcb)
            self.scheduler.add(pcb)
        else:
            self.queueWait.add(pcb)
            
    def notify(self,size):
        while not self.queueWait.empty():
            pcb=self.queueWait.get()
            if(pcb.size<=size):
                self.memory.allocateMemory(pcb)
                self.scheduler.add(pcb)
                break
                
            