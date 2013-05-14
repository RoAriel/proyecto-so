'''
Created on 29/04/2013

@author: Di Meglio
'''

import scheduler

class CPU():
    
    def __init__(self,managerIntrruptions,memory,mode):
        self.managerIntrruptions=managerIntrruptions
        self.pcb=None
        self.memory=memory
        self.mode=mode
    

    def setProcess(self,pcb):
        self.pcb=pcb
        
    def click(self):
        
        if( self.mode.isModeUser()): 
            self.pcd.setState('Running')
            pc=self.pcb.getPC()+self.pcd.getDirIni()
            self.pcd.addPc()
            instruction=self.memory.get(pc) 
            instruction.execute(self.managerIntrruptions)
        