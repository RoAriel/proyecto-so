'''
Created on 13/05/2013

@author: usuario
'''
import scheduler as s
import clock 
import interruptions as i

class Kernel():
    
    def _init_(self,cpu,memory,managerInterruptions,policy,disk,mode):
        self.cpu=cpu
        self.memory=memory
        self.managerInterruptions=managerInterruptions
        self.scheduler=s.Scheduler(policy)
        self.disk=disk
        self.mode=mode
        self.clock=clock(self.scheduler.getTimer())
        i.ManagerInterruptions.config(self.scheduler,self.mode.self.cpu)
        
    def executeProgram(self,nameProgram):
        pass
    
    def stop(self):
        pass
    
    def start(self):
        self.clock.start()
         
         

class Mode():
    
    def _init_(self):
        #true=mode user
        #false=mode kernel
        self.mode=True
        
    def setModeUser(self):
        self.mode=True
        
    def setModeKernel(self):
        self.mode=False
        
    def isModeUser(self):
        return self.mode
    
    
