'''
Created on 13/05/2013

@author: rodrigo
'''

class Program():
    def __init__(self, listInstruccion, processCounter,):
        self.myProcess = processCounter

# el pcb va a parar a la tabla de PCB'S  en el kernel
# cuando termina el proceso guado al ese proceso en PCB'S en DeadTable 

class BloqueDeControlDeProceso():
    def __init__(self, procount, estado, stack, idproces):
        self.pc= procount
        self.estado= None 
        self.stack = 'direccion de alojamiento'
        self.pid=idproces
    
    
