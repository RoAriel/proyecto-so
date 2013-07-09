'''
Created on 13/05/2013

@author: usuario
'''
import scheduler as s
import clock as c
import interruptions as i
from hardware import PCB
from hardware import PidGenerator
import devices
from plp import PLP
from processAndProgram import State

class Kernel():
    
    def __init__(self,cpu,memoryPhysical,memoryLogic,policy,disk,mode):
        self.memoryLogic=memoryLogic
        self.cpu=cpu
        self.PhysicalMemory=memoryPhysical
        self.logicMemory=memoryLogic
        self.scheduler=s.Scheduler(policy)
        self.disk=disk
        self.mode=mode
        self.clock=c.Clock(self.cpu,self.scheduler.getTimer())
        self.managerDevices=devices.ManagerDivices(self.scheduler,cpu)
        self.plp=PLP(memoryLogic,self.scheduler,cpu)
        memoryLogic.plp=self.plp
        i.ManagerInterruptions.config(self.scheduler,self.mode,self.cpu,self.clock.timer,self,self.managerDevices)
    
        
    def executeProgram(self,pathProgram):
        if(self.disk.programExists(pathProgram)):
            pcb=PCB(pathProgram,PidGenerator.getPid(),self.disk.getSizeProgram(pathProgram))
            self.addPcb(pcb)
    
    
    def addProgram(self,program):
        self.disk.addProgram(program)       
    
    def stop(self):
        self.clock.stop()
    
    def start(self):
        self.clock.start()
        
    def addPcb(self,pcb):
        self.mode.setModeKernel()
        self.plp.allocateMemory(pcb)
        self.mode.setModeUser()
        
    def swapIn(self,page,pcb):
        diskBlock=self.disk.getBlock(page,pcb.pid,pcb.pathProgram)
        
        frame=self.memoryLogic.getFrame()

        self.memoryLogic.allocateInstructionInMemoryPhysical(diskBlock.getInstructions(),frame)
        page.inMemory=True
        
        """Se debe registrar el el algoritmo de remplazo la pagina 
           que fue cargada a memoria
        """
        self.memoryLogic.replacementAlgorithms.register(page,pcb)
        """se debe actualizar la pagina con el frame en la tabla de paginas"""
        self.memoryLogic.updateTablePageOf(pcb,page,frame)
        
    def swapOut(self,page,pcb,frame):
        instructions=self.memoryLogic.getDataOfPhysical(frame)
        self.disk.save(pcb,page,instructions)
        page.inMemory=False
        
        
    def kill(self,pcb):
        self.memoryLogic.kill(pcb)
        self.scheduler.kill(pcb)
        pcb.state=State.finished
        
class Mode():
    
    def __init__(self):
        #true=mode user
        #false=mode kernel
        self.mode=True
        
    def setModeUser(self):
        self.mode=True
        
    def setModeKernel(self):
        self.mode=False
        
    def isModeUser(self):
        return self.mode
    


