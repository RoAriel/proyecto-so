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

mode=kernel.Mode()
physicalMemory=hardware.PhysicalMemory(40)
disk=hardware.Disk(8)
paging=logicMemory.Paging(hardware.Disk(8),physicalMemory,logicMemory.FIFO())
cpu=CPU(paging,mode)
scheduler=scheduler.SJF(True)


k=kernel.Kernel(cpu,physicalMemory,paging,scheduler,disk,mode)
k.start()

"""Creacion de programas"""
myProgram=processAndProgram.Program('Home/user/myProgram',[i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram1=processAndProgram.Program('Home/user/myProgram1',[i.Cpu(),i.Cpu(),i.Finalize()])
myProgram2=processAndProgram.Program('Home/user/myProgram2',[i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram3=processAndProgram.Program('Home/user/myProgram3',[i.Cpu(),i.Cpu(),i.Finalize()])


k.addProgram(myProgram)
k.addProgram(myProgram1)
k.addProgram(myProgram2)
k.addProgram(myProgram3)





k.executeProgram('Home/user/myProgram')
#k.executeProgram('Home/user/myProgram')
#k.executeProgram('Home/user/myProgram')
#k.executeProgram('Home/user/myProgram')


time.sleep(15)

print k.disk.swap
print k.memoryLogic.pagesOfPcb
print k.memoryLogic.takenFrame
print k.memoryLogic. replacementAlgorithms.queue.empty()
print k.memoryLogic. replacementAlgorithms.takenPage


