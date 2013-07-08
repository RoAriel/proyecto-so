'''
Created on 24/05/2013

@author: Di Meglio
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

mode=kernel.Mode()
physicalMemory=hardware.PhysicalMemory(50)
disk=hardware.Disk(8)
acont=logicMemory.ContinuousAssignment(disk, physicalMemory,logicMemory.BestFit())
cpu=CPU(acont,mode)
scheduler=scheduler.FCFS()


k=kernel.Kernel(cpu,physicalMemory,acont,scheduler,disk,mode)
# k.start()

"""Creacion de programas"""
path='Home/user/myProgram'
myProgram=processAndProgram.Program(path,[i.Cpu(),i.IO(TypeDevice.monitor),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram1=processAndProgram.Program('Home/user/myProgram1',[i.Cpu(),i.Cpu(),i.Finalize()])
myProgram2=processAndProgram.Program('Home/user/myProgram2',[i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram3=processAndProgram.Program('Home/user/myProgram3',[i.Cpu(),i.Cpu(),i.Finalize()])



k.addProgram(myProgram)
k.addProgram(myProgram1)
k.addProgram(myProgram2)
k.addProgram(myProgram3)


pcb=processAndProgram.PCB('Home/user/myProgram',0,11)
k.plp.allocateMemory(pcb)
pcb6=processAndProgram.PCB('Home/user/myProgram2',1,6)
k.plp.allocateMemory(pcb6)
pcb3=processAndProgram.PCB('Home/user/myProgram3',2,3)
k.plp.allocateMemory(pcb3)
pcb=processAndProgram.PCB('Home/user/myProgram',4,11)
k.plp.allocateMemory(pcb)
pcb=processAndProgram.PCB('Home/user/myProgram',5,11)
k.plp.allocateMemory(pcb)
acont.kill(pcb3)
pcb=processAndProgram.PCB('Home/user/myProgram',6,11)
k.plp.allocateMemory(pcb)
pcb=processAndProgram.PCB('Home/user/myProgram',7,11)
k.plp.allocateMemory(pcb)
acont.kill(pcb6)
acont.show()

"""

import threading  as t

class a(t.Thread):
    
    def run(self):
        for i in range(500):
            time.sleep(1)
            k.executeProgram('Home/user/myProgram')

class b(t.Thread):
    
    def run(self):
        for i in range(377):
#             time.sleep(1)
            k.executeProgram('Home/user/myProgram1')

class c(t.Thread):
    
    def run(self):
        for i in range(1050):
            time.sleep(1)
            k.executeProgram('Home/user/myProgram3')    

a().run()
b().run()
c().run()

"""

"""
time.sleep(65)

print k.disk.swap
print k.memoryLogic.pagesOfPcb
print k.memoryLogic.takenFrame
print k.memoryLogic. replacementAlgorithms.queue.empty()
print k.memoryLogic. replacementAlgorithms.takenPage
"""