'''

Created on 15/05/2013

@author: Di Meglio
'''

class ManagerInterruptions():
    
    
    def _init_(self,scheduler,cpu,mode):
        self.scheduler=scheduler
        self.cpu=cpu
        self=mode=mode
        self.mapInterruption={'timeOut':self.timeOut}
        
    def throwInterruption(self,interruption):
        self.mapInterruption[interruption]()
        
    def timeOut(self):
        self.mode.setModeKernel()
        self.scheduler.add(self.cpu.pcb)
        self.cpu.setProcess(self.scheduler.get())
        self.mode.setModeUser()

class Interruption():
    timeOut='timeOut'
    
    
"""
EJEMPLO DE USO
MI= ManagerInterruption(scheduler(),cpu(),mode())
MI.throwInterruption(Interruption.timeOut)
"""
