'''
Created on 24/05/2013

@author: Di Meglio
'''
import threading  as t
import kernel
from hardware import CPU
import scheduler
import hardware
import processAndProgram
import instructions as i 
import time
import random
import logicMemory
import time
from devices import TypeDevice

mode=kernel.Mode()
physicalMemory=hardware.PhysicalMemory(1600)
disk=hardware.Disk(8)
paging=logicMemory.Paging(hardware.Disk(8),physicalMemory,logicMemory.FIFO())
cpu=CPU(paging,mode)
scheduler=scheduler.SJF(True)


k=kernel.Kernel(cpu,physicalMemory,paging,scheduler,disk,mode)
k.start()

"""Creacion de programas"""
myProgram=processAndProgram.Program('Home/user/myProgram',[i.Cpu(),i.IO(TypeDevice.monitor),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram1=processAndProgram.Program('Home/user/myProgram1',[i.Cpu(),i.Cpu(),i.Finalize()])
myProgram2=processAndProgram.Program('Home/user/myProgram2',[i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram3=processAndProgram.Program('Home/user/myProgram3',[i.Cpu(),i.Cpu(),i.Finalize()])


k.addProgram(myProgram)
k.addProgram(myProgram1)
k.addProgram(myProgram2)
k.addProgram(myProgram3)

import threading  as t

class a(t.Thread):
    
    def run(self):
        for i in range(500):
            time.sleep(1)
            k.executeProgram('Home/user/myProgram')

class b(t.Thread):
    
    def run(self):
        for i in range(377):
            time.sleep(1)
            k.executeProgram('Home/user/myProgram1')

class c(t.Thread):
    
    def run(self):
        for i in range(1050):
            time.sleep(1)
            k.executeProgram('Home/user/myProgram3')    
"""
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

b=b()
b.nombre

