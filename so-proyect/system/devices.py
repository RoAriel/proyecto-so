'''
Created on 09/06/2013

@author: CABJ
'''
import threading  as t
import time
import random


class ManagerDivices():
    def __init__(self,kernel):
        self.divices={TypeDevice.keyboard:DeviceIO(TypeDevice.keyboard,kernel),
                       TypeDevice.monitor:DeviceIO(TypeDevice.monitor,kernel),
                       TypeDevice.printer: DeviceIO(TypeDevice.printer,kernel)
                       }
        
    def getDeviceIO(self,aDevice):
        return self.divices[aDevice]

    def add(self,pcb,aDevice):
        self.getDeviceIO(aDevice).add(pcb)


class DeviceIO():
    
    def __init__(self,type,kernel):
        self.type=type
        self.kernel=kernel
        
    def add(self,pcb):
        Controller(pcb,self.kernel).start()
          
        
        
"""Se encarga de simular que tiempo de IO que tarda la instruccion""" 
class Controller(t.Thread):
    
    def __init__(self,pcb,kernel):
        t.Thread.__init__(self)
        self.pcb=pcb
        self.kernel=kernel
        
    def run(self):
        time.sleep(random.randrange(1,15))
        self.kernel.addPcb(self.pcb)
    


class TypeDevice():
    monitor="monitor"
    keyboard="keyboard"
    printer="printer"