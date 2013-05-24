'''
Created on 29/04/2013

@author: Di Meglio
'''

import scheduler
from interruptions  import Interruption 
from process import State

class CPU():
    
    
    def __init__(self,memory,mode):
        self.memory=memory
        self.mode=mode
        self.pcb=None
    

    def setProcess(self,pcb):
        self.pcb=pcb
        
    def click(self):
        
        if( self.mode.isModeUser() & (self.pcb is not None)): 
            self.pcb.state=State.running
            pc=self.pcb.pc+self.pcb.initialDirection
            self.pcb.addPc()
            instruction=self.memory.getData(pc) 
            instruction.execute(self.pcb)
    
            
            