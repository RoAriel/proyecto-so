'''
Created on 09/06/2013

@author: CABJ
'''
import threading  as t
import time
import random

class DeviceIO():
    
    def __init__(self,type,scheduler):
        self.type=type
        self.schedueler=scheduler
        
    def add(self,pcb):
        Controller(pcb,self.schedueler).start()
          
        
        
        
class Controller(t.thread):
    
    def __init__(self,pcb,scheduler):
        self.pcb=pcb
        self.scheduler=scheduler
        
    def run(self):
        time(random.randrange(1,15))
        self.scheduler.add(self.pcb)
    

class TypeDivice():
    monitor="monitor"
    keyboard="keyboard"
    printer="printer"