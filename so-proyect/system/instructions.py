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
from interruptions import GloabalContext
from interruptions import IOContext

class Instruction():
    
    def execute(self,managerInterruptions,pcb):
        pass
    
    
class IO(Instruction):
    
    def __init__(self,divice=None):
        self.divice=divice
        
    def execute(self,pcb):
        pcb.sate=State.wait
        i.ManagerInterruptions.throwInterruption(Interruption.IO,IOContext(pcb,self.divice))
#
        
        
        
class Finalize(Instruction):

    def execute(self,pcb):
        pcb.sate=State.finished
        i.ManagerInterruptions.throwInterruption(Interruption.pcbFinalize,GloabalContext(pcb))
        print 'process id:',pcb.pid ,'finlize'
        
        
class Cpu(Instruction):

    def execute(self,pcb):
        print 'process id:',pcb.pid ,'execute'
        pass