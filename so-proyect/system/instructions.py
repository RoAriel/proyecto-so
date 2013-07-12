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
        logging.info('process id: %s IO',pcb.pid)
        logging.info('program %s',pcb.pathProgram )

        
        
"""Todos los programas deben terminar con esta instruccion"""       
class Finalize(Instruction):

    def execute(self,pcb):
        pcb.sate=State.finished
        i.ManagerInterruptions.throwInterruption(Interruption.pcbFinalize,GloabalContext(pcb))
        logging.info('process id: %s finished',pcb.pid)
        logging.info('program %s',pcb.pathProgram )
        
        
        
class Cpu(Instruction):

    def execute(self,pcb):
        logging.info('process id: %s execute',pcb.pid)
        logging.info('program %s',pcb.pathProgram )

