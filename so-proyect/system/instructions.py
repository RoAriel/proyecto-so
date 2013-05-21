'''
Created on 19/05/2013

@author: CABJ
'''
import threading  as t
from interruptions  import Interruption 
import random
import time
from process import State

class Instruction():
    
    def execute(self,managerInterruptions,pcb):
        pass
    
    
class IO(Instruction,t.Thread):
    
    def execute(self,managerInterruptions,pcb):
        pcb.sate=State.wait
        managerInterruptions.throwInterruption(Interruption.IO)
        self.run()
        
    def run(self):
        time.sleep(random.random(4,10))
        
        
class Finalize(Instruction):
    
    def execute(self,managerInterruptions,pcb):
        pcb.sate=State.finished
        managerInterruptions.throwInterruption(Interruption.pcbFinalize)