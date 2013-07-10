'''
Created on 19/05/2013

@author: j di meglio
'''
import threading  as t
from interruptions  import Interruption 
import interruptions as i
import random
import time
from processAndProgram import State
from interruptions import GloabalContext
from interruptions import IOContext
import logging

class Instruction():
    
    def execute(self,managerInterruptions,pcb):
        pass
    
    
class IO(Instruction):
    
    def __init__(self,device=None):
        self.device=device
        
    def execute(self,pcb):
        pcb.sate=State.wait
        i.ManagerInterruptions.throwInterruption(Interruption.IO,IOContext(pcb,self.device))
        logging.info(('process id:',pcb.pid ,'IO'))
        logging.info(('program ',pcb.pathProgram ))

        
        
        
class Finalize(Instruction):

    def execute(self,pcb):
        pcb.sate=State.finished
        i.ManagerInterruptions.throwInterruption(Interruption.pcbFinalize,GloabalContext(pcb))
        logging.info(('process id:',pcb.pid ,'finished'))
        logging.info(('program ',pcb.pathProgram ) ) 
        
        
        
class Cpu(Instruction):

    def execute(self,pcb):
        logging.info(('process id:',pcb.pid ,'execute'))
        logging.info(('program ',pcb.pathProgram )) 

