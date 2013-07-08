'''
Created on 09/06/2013

@author: CABJ
'''
import threading  as t
import time
import random
from processAndProgram import State

class ManagerDivices():
    def __init__(self,scheduler,cpu):
        self.divices={TypeDevice.keyboard:DeviceIO(TypeDevice.keyboard,scheduler,cpu),
                       TypeDevice.monitor:DeviceIO(TypeDevice.monitor,scheduler,cpu),
                       TypeDevice.printer: DeviceIO(TypeDevice.printer,scheduler,cpu)
                       }
        
    def getDeviceIO(self,aDevice):
        return self.divices[aDevice]

    def add(self,pcb,aDevice):
        self.getDeviceIO(aDevice).add(pcb)


class DeviceIO():
    
    def __init__(self,type,scheduler,cpu):
        self.type=type
        self.scheduler=scheduler
        self.cpu=cpu
        
    def add(self,pcb):
        Controller(pcb,self.scheduler,self.cpu).start()
          
        
        
"""Se encarga de simular que tiempo de IO  tarda """ 
class Controller(t.Thread):
    
    def __init__(self,pcb,scheduler,cpu):
        t.Thread.__init__(self)
        self.pcb=pcb
        self.scheduler=scheduler
        self.cpu=cpu
        
    def run(self):
        time.sleep(random.randrange(1,15))
        self.scheduler.add(self.pcb,self.cpu)
    


class TypeDevice():
    monitor="monitor"
    keyboard="keyboard"
    printer="printer"