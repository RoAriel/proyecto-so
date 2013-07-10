'''
Created on 09/07/2013

@author: CABJ
'''
import threading  as t
import system.kernel as kernel
from system.hardware import CPU
import system.scheduler as scheduler
import system.hardware as hardware
import system.processAndProgram as processAndProgram
import system.instructions as i 
import time
import random
import system.logicMemory as logicMemory
import time
from system.devices import TypeDevice 



class Console():
    
    def __init__(self):
        self.commands={Command.kill: self.kill,Command.ps:self.ps,Command.execute:self.executeProgram,Command.exit:
                       self.exit,Command.start:self.startKernel,Command.stop:self.stopKernel}
        self.kernel=None
        self.running=True
        
    def start(self):
        self.generateKernel()
        self.kernel.start()
        self.run()
    
    def run(self):
        while(self.running):
            input=raw_input('>')
            input=input.split()
            try:
                self.execute(input)
            except Exception , e:
                print e
            
    def execute(self,input):
        try:
            behavior=self.commands[input[0]]
        except Exception ,e:
            raise Exception('El comando no existe')
        behavior(input)
        
    def validateNumberParam(self,n1,n2):
        if(n1 != n2):
            raise Exception('Cantidad de argumentos invalido')
        
        
    def startKernel(self,input):
        self.validateNumberParam(len(input)-1, 0)
        self.kernel.start()
        
    def stopKernel(self,input):
        self.validateNumberParam(len(input)-1, 0)
        self.kernel.stop()
        
    def executeProgram(self,input):
        self.validateNumberParam(len(input)-1, 1)
        self.kernel.executeProgram(input[1])
        
    def ps(self,input):
        self.validateNumberParam(len(input)-1, 0)
        self.kernel.showProcess()
    
    def exit(self,input):
        self.validateNumberParam(len(input)-1, 0)
        self.running=False
        print 'Bye'
    
    def generateKernel(self):
        mode=kernel.Mode()
        physicalMemory=hardware.PhysicalMemory(16)
        disk=hardware.Disk(8)
        acont=logicMemory.ContinuousAssignment(disk, physicalMemory,logicMemory.BestFit())
        cpu=CPU(acont,mode)
        schedr=scheduler.FCFS()
        
        """Algunos programas por defecto"""
        myProgram=processAndProgram.Program('Home/user/myProgram',[i.Cpu(),i.IO(TypeDevice.monitor),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
        myProgram1=processAndProgram.Program('Home/user/myProgram1',[i.Cpu(),i.Cpu(),i.Finalize()])
        myProgram2=processAndProgram.Program('Home/user/myProgram2',[i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
        myProgram3=processAndProgram.Program('Home/user/myProgram3',[i.Cpu(),i.Cpu(),i.Finalize()])
        
        self.kernel=kernel.Kernel(cpu,physicalMemory,acont,schedr,disk,mode)

        """se agregan los programas"""
        self.kernel.addProgram(myProgram)
        self.kernel.addProgram(myProgram1)
        self.kernel.addProgram(myProgram2)
        self.kernel.addProgram(myProgram3)
        
    def kill(self,input):
        self.validateNumberParam(len(input)-1, 1)
        self.kernel.killPcb(int(input[1]))

class Command():
    
    start='start'
    stop='stop'
    execute='execute'
    exit='exit'
    ps='ps'
    kill='kill'
    
    
console=Console()
console.start()