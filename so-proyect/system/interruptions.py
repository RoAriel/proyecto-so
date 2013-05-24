'''

Created on 15/05/2013

@author: Di Meglio
'''
from process import State

#la intencion de que esta clase sea estatica  es porque en muchas partes
#del sistema se requiere

class ManagerInterruptions():
    
    #es el pcb que debe expropiar la cpu
    pcbExpropiation=None
    
    cpu=None
    mode=None
    scheduler=None
    mapInterruption={"""Interruption.timeOut: ManagerInterruptions.timeOut,
                              Interruption.IO: ManagerInterruptions.IO,
                              Interruption.pcbFinalize:ManagerInterruptions.pcbFinalize,
                              Interruption.expropiation:ManagerInterruptions.expropiation"""}
    
    @classmethod  
    def config(self,scheduler,mode,cpu):
        ManagerInterruptions.mode=mode
        ManagerInterruptions.scheduler=scheduler  
        ManagerInterruptions.cpu=cpu  
        
    @classmethod      
    def throwInterruption(self,interruption):
        ManagerInterruptions.mapInterruption[interruption]()
    
    @classmethod     
    def timeOut(self):
        ManagerInterruptions.mode.setModeKernel()
        ManagerInterruptions.scheduler.add(ManagerInterruptions.cpu.pcb)
        ManagerInterruptions.cpu.setProcess(ManagerInterruptions.scheduler.get())
        ManagerInterruptions.mode.setModeUser()
    
    @classmethod     
    def IO(self):
        pcb=self.cpu.pcb
        pcb.setState(State.wait)
        ManagerInterruptions.queueWait.add(pcb)
        ManagerInterruptions.timeOut()
    
    @classmethod     
    def pcbFinalize(self):
        ManagerInterruptions.mode.setModeKernel()
        ManagerInterruptions.cpu.pcb.setSate(State.finished)
        ManagerInterruptions.cpu.setProcess(ManagerInterruptions.scheduler.get())
        ManagerInterruptions.mode.setModeUser()
    
    @classmethod      
    def expropiation(self):
        print 'ddd'

class Interruption():
    timeOut='timeOut'
    IO='IO'
    pcbFinalize="pcbFinalize"
    expropiation="expropiatio"
    
"""
EJEMPLO DE USO
throwInterruption(Interruption.timeOut)
"""


        
