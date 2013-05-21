'''

Created on 15/05/2013

@author: Di Meglio
'''
from process import State

class ManagerInterruptions():
    
    
    def _init_(self,scheduler,cpu,mode,queueWait):
        self.scheduler=scheduler
        self.cpu=cpu
        self=mode=mode
        self.queueWait=queueWait
        self.mapInterruption={Interruption.timeOut:self.timeOut,Interruption.IO:self.IO,
                              Interruption.pcbFinalize:self.pcbFinalize}
        
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
        
    def pcbFinalize(self):
        self.mode.setModeKernel()
        self.cpu.pcb.setSate(State.finished)
        self.cpu.setProcess(self.scheduler.get())
        self.mode.setModeUser()
         

class Interruption():
    timeOut='timeOut'
    IO='IO'
    pcbFinalize="pcbFinalize"
    
"""
EJEMPLO DE USO
MI= ManagerInterruption(scheduler(),cpu(),mode())
MI.throwInterruption(Interruption.timeOut)
"""
