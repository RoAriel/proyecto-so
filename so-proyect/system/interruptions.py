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
    
    timer=None
    cpu=None
    mode=None
    scheduler=None
    disk=None
    kernel=None
    
    page=None
    paging=None     
    pcb=None
    
    mapInterruption=None

    
    @classmethod  
    def config(self,scheduler,mode,cpu,timer,kernel):
        ManagerInterruptions.kernel=kernel
        ManagerInterruptions.timer=timer
        ManagerInterruptions.mode=mode
        ManagerInterruptions.scheduler=scheduler  
        ManagerInterruptions.cpu=cpu  
        ManagerInterruptions.mapInterruption={Interruption.timeOut: ManagerInterruptions.timeOut,
                              Interruption.IO: ManagerInterruptions.IO,
                              Interruption.pcbFinalize:ManagerInterruptions.pcbFinalize,
                              Interruption.expropiation:ManagerInterruptions.expropiation,
                              Interruption.pageFault:ManagerInterruptions.pageFault}
        
    @classmethod      
    def throwInterruption(self,interruption):
        ManagerInterruptions.mapInterruption[interruption]()
    
    @classmethod     
    def timeOut(self):
        ManagerInterruptions.mode.setModeKernel()
        if(ManagerInterruptions.cpu.pcb is not None):
            ManagerInterruptions.scheduler.add(ManagerInterruptions.cpu.pcb,ManagerInterruptions.cpu)
        ManagerInterruptions.cpu.setProcess(ManagerInterruptions.scheduler.get())
        ManagerInterruptions.mode.setModeUser()
    
    @classmethod     
    def IO(self):
        ManagerInterruptions.mode.setModeKernel()
        pcb=self.cpu.pcb
        pcb.state=State.wait
#       ManagerInterruptions.queueWait.add(pcb)
        ManagerInterruptions.timer.resetQuantum()
        ManagerInterruptions.timeOut()
    
    @classmethod     
    def pcbFinalize(self):
        ManagerInterruptions.mode.setModeKernel()
        ManagerInterruptions.cpu.pcb.state=State.finished
        ManagerInterruptions.cpu.setProcess(ManagerInterruptions.scheduler.get())
        ManagerInterruptions.timer.resetQuantum()
        ManagerInterruptions.mode.setModeUser()
    
    @classmethod      
    def expropiation(self):
        ManagerInterruptions.mode.setModeKernel()
        ManagerInterruptions.cpu.pcb.state=State.ready
        ManagerInterruptions.scheduler.addAsReady(ManagerInterruptions.cpu.pcb)
        ManagerInterruptions.cpu.pcb=ManagerInterruptions.pcbExpropiation
        ManagerInterruptions.timer.resetQuantum()
        ManagerInterruptions.mode.setModeUser()
        
    
    @classmethod      
    def pageFault(self):
        ManagerInterruptions.mode.setModeKernel()
        self.kernel.swapIn(self.page,self.pcb)
        ManagerInterruptions.mode.setModeUser()


class Interruption():
    timeOut='timeOut'
    IO='IO'
    pcbFinalize="pcbFinalize"
    expropiation="expropiatio"
    pageFault='pageFault'
    
"""
EJEMPLO DE USO
throwInterruption(Interruption.timeOut)
"""

"""Estas clases sirven para agrupar los objetos que va a necesitar cada interrupcion,por ahora no esta en uso
  pero la idea es que el managerInterruption tenga un map  con estos contextos 
"""
class ContextExpropiation():
    
    def __init__(self,pcb):
        self.pcb=pcb

class ContextPageFault():
    
    def __init__(self,paging,pcb,page):
        self.paging=paging
        self.pcb=pcb
        self.page=page
        
class ContextIO():
    
    def __init__(self,pcb,instruction):
        self.pcb=pcb
        self.instruction=instruction
        
