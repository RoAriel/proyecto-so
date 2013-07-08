'''

Created on 15/05/2013

@author: Di Meglio
'''
from processAndProgram import State

#la intencion de que esta clase sea estatica  es porque en muchas partes
#del sistema se requiere

class ManagerInterruptions():
    
    #es el pcb que debe expropiar la cpu
    
    timer=None
    cpu=None
    mode=None
    scheduler=None
    disk=None
    kernel=None
    managerDevices=None
    
    mapInterruption=None

    
    @classmethod  
    def config(self,scheduler,mode,cpu,timer,kernel,managerDevices):
        ManagerInterruptions.managerDevices=managerDevices
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
    def throwInterruption(self,interruption,context):
        ManagerInterruptions.mapInterruption[interruption](context)
    
    @classmethod     
    def timeOut(self,context):
        ManagerInterruptions.mode.setModeKernel()
        if(ManagerInterruptions.cpu.pcb is not None):
            ManagerInterruptions.scheduler.add(ManagerInterruptions.cpu.pcb,ManagerInterruptions.cpu)   
        ManagerInterruptions.cpu.setProcess(ManagerInterruptions.scheduler.get())
        ManagerInterruptions.mode.setModeUser()
        print 'interruptins timeOut'
    
    @classmethod     
    def IO(self,context):
        ManagerInterruptions.mode.setModeKernel()
        context.pcb.state=State.wait
        ManagerInterruptions.managerDevices.add(context.pcb,context.device)
        ManagerInterruptions.timer.resetQuantum()
        ManagerInterruptions.cpu.setProcess(ManagerInterruptions.scheduler.get())
        ManagerInterruptions.mode.setModeUser()
        print 'interruptions IO'
    
    @classmethod     
    def pcbFinalize(self,context):
        ManagerInterruptions.mode.setModeKernel()
        context.pcb.state=State.finished
        ManagerInterruptions.cpu.setProcess(ManagerInterruptions.scheduler.get())
        ManagerInterruptions.kernel.kill(context.pcb)
        ManagerInterruptions.timer.resetQuantum()
        ManagerInterruptions.mode.setModeUser()
        print 'interruptins finished'
    
    @classmethod      
    def expropiation(self,context):
        ManagerInterruptions.mode.setModeKernel()
        ManagerInterruptions.cpu.pcb.state=State.ready
        ManagerInterruptions.scheduler.addAsReady(ManagerInterruptions.cpu.pcb)
        ManagerInterruptions.cpu.pcb=context.pcb
        ManagerInterruptions.timer.resetQuantum()
        ManagerInterruptions.mode.setModeUser()
        print 'interruptins expropiation'
    
    @classmethod      
    def pageFault(self,context):
        ManagerInterruptions.mode.setModeKernel()
        self.kernel.swapIn(context.page,context.pcb)
        ManagerInterruptions.mode.setModeUser()
        print 'interruptins pageFault'



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

class GloabalContext():
    def __init__(self,pcb):
        self.pcb=pcb


class PageFaultContext():
    
    def __init__(self,pcb,page):
        self.pcb=pcb
        self.page=page
        
class IOContext():
    
    def __init__(self,pcb,device):
        self.pcb=pcb
        self.device=device
