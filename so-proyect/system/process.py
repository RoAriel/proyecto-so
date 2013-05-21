'''
Created on 13/05/2013

@author: rodrigo
'''

class Program():
    def __init__(self, listInstruccion, processCounter,):
        self.myProcess = processCounter

# el pcb va a parar a la tabla de PCB'S  en el kernel
# cuando termina el proceso guado al ese proceso en PCB'S en DeadTable 

class PCB():
    def __init__(self, pc, stack, pid):
        self.pc= pc
        self.estado=State.new
        self.stack = 'direccion de alojamiento'
        self.pid=pid
    
    
class State():
    new="New"
    running="Running"
    wait="Wait"
    finished="Finished"
    ready="Ready"
    
