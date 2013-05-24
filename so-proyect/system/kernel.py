'''
Created on 13/05/2013

@author: usuario
'''
import scheduler as s
import clock as c
import interruptions as i

class Kernel():
    
    def __init__(self,cpu,memory,policy,disk,mode):
        self.cpu=cpu
        self.memory=memory
        self.scheduler=s.Scheduler(policy)
        self.disk=disk
        self.mode=mode
        self.clock=c.Clock(None)
        self.clock.cpu=self.cpu
        self.clock.timer=self.scheduler.getTimer()
        #i.ManagerInterruptions.config(self.scheduler,self.mode.self.cpu)
    
        
    def executeProgram(self,nameProgram):
        pass
    
    def stop(self):
        pass
    
    def start(self):
        self.clock.start()
        
    def addPcb(self,pcb):
        if(self.cpu.pcb is None):
            self.cpu.pcb=pcb
        else:
            self.scheduler.add(pcb)
           
         

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
    

    
