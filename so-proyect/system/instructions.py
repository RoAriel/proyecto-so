'''
Created on 19/05/2013

@author: CABJ
'''
import threading  as t
from interruptions  import Interruption 
import interruptions as i
import random
import time
from process import State


class Instruction():
    
    def execute(self,managerInterruptions,pcb):
        pass
    
    
class IO(Instruction,t.Thread):
    
    def execute(self,pcb):
        pcb.sate=State.wait
        i.ManagerInterruptions.throwInterruption(Interruption.IO)
#         self.run()
        
    def run(self):
        time.sleep(random.random(4,10))
        
        
class Finalize(Instruction):

    def execute(self,pcb):
        pcb.sate=State.finished
        i.ManagerInterruptions.throwInterruption(Interruption.pcbFinalize)
        
        
class Cpu(Instruction):

    def execute(self,pcb):
        pass