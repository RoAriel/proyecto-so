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
    

    def setProcess(self,pcb):
        self.pcb=pcb
        
    def click(self):
        
        if( self.mode.isModeUser() & self.pcb is not None): 
            self.pcd.setState(State.running)
            pc=self.pcb.getPC()+self.pcd.getDirIni()
            self.pcd.addPc()
            instruction=self.memory.get(pc) 
            instruction.execute()
    
            
            