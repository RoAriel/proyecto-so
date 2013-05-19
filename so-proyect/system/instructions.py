'''
Created on 19/05/2013

@author: CABJ
'''
import threading  as t
from interruptions  import Interruption 

class Instruction():
    
    def execute(self,managerInterruptions):
        pass
    
    
class IO(Instruction,t.Thread):
    
    def execute(self,managerInterruptions):
        self.run()
        
    def run(self):
        pass
        
        
class Finalize(Instruction):
    
    def execute(self,managerInterruptions):
        managerInterruptions.throwInterruption(Interruption.timeOut)