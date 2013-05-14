'''
Created on 13/05/2013

@author: usuario
'''


class Kernel():
    
    def _init_(self,cpu,memory,managerInterruptions,policy):
        self.cpu=cpu
        self.memory=memory
        self.managerInterruptions=managerInterruptions
        self.policy=policy
         
         

class Mode():
    
    def _init_(self):
        #true=mode user
        #false=mode kernel
        self.mode=True
        
    def setModeUser(self):
        self.mode=True
        
    def setMdeKernel(self):
        self.mode=False
        
    def isMOdeUser(self):
        return self.mode