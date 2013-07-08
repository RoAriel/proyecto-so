'''
Created on 19/05/2013

@author: CABJ
'''
import threading  as t
from interruptions  import Interruption 
import interruptions as i
import random
import time
from processAndProgram import State
from interruptions import GloabalContext
from interruptions import IOContext

class Instruction():
    
    def execute(self,managerInterruptions,pcb):
        pass
    
    
class IO(Instruction):
    
    def __init__(self,device=None):
        self.device=device
        
    def execute(self,pcb):
        pcb.sate=State.wait
        i.ManagerInterruptions.throwInterruption(Interruption.IO,IOContext(pcb,self.device))
        print 'process id:',pcb.pid ,'IO'
        print 'program ',pcb.pathProgram     
        
        
        
class Finalize(Instruction):

    def execute(self,pcb):
        pcb.sate=State.finished
        i.ManagerInterruptions.throwInterruption(Interruption.pcbFinalize,GloabalContext(pcb))
        print 'process id:',pcb.pid ,'finished'
        print 'program ',pcb.pathProgram
        
        
class Cpu(Instruction):

    def execute(self,pcb):
        print 'process id:',pcb.pid ,'execute'
        print 'program ',pcb.pathProgram

  