'''

Created on 15/05/2013

@author: Di Meglio
'''

class ManagerInterruptions():
    
    
    def _init_(self,scheduler,cpu,mode,queueWait):
        self.scheduler=scheduler
        self.cpu=cpu
        self=mode=mode
        self.queueWait=queueWait
        self.mapInterruption={'timeOut':self.timeOut,"IO":self.IO}
        
    def throwInterruption(self,interruption):
        self.mapInterruption[interruption]()
        
    def timeOut(self):
        self.mode.setModeKernel()
        self.scheduler.add(self.cpu.pcb)
        self.cpu.setProcess(self.scheduler.get())
        self.mode.setModeUser()
        
    def IO(self):
        pcb=self.cpu.pcb
        self.queueWait.add(pcb)
        self.timeOut()
        

class Interruption():
    timeOut='timeOut'
    IO='IO'
    
    
"""
EJEMPLO DE USO
MI= ManagerInterruption(scheduler(),cpu(),mode())
MI.throwInterruption(Interruption.timeOut)
"""
