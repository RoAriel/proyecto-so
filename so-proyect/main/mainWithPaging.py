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


"""
Se crea un kernel con policy FCFS,sistema de paginacion de memoria

"""

mode=kernel.Mode()
physicalMemory=hardware.PhysicalMemory(1600)
disk=hardware.Disk(8)
paging=logicMemory.Paging(disk,physicalMemory,logicMemory.FIFO())
cpu=CPU(paging,mode)
scheduler=scheduler.FCFS()


k=kernel.Kernel(cpu,physicalMemory,paging,scheduler,disk,mode)
k.start()

"""Creacion de programas"""
myProgram=processAndProgram.Program('Home/user/myProgram',[i.Cpu(),i.IO(TypeDevice.monitor),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram1=processAndProgram.Program('Home/user/myProgram1',[i.Cpu(),i.Cpu(),i.Finalize()])
myProgram2=processAndProgram.Program('Home/user/myProgram2',[i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
myProgram3=processAndProgram.Program('Home/user/myProgram3',[i.Cpu(),i.Cpu(),i.Finalize()])


"""se agregan los programas"""
k.addProgram(myProgram)
k.addProgram(myProgram1)
k.addProgram(myProgram2)
k.addProgram(myProgram3)



"""y se ejecutan"""
k.executeProgram('Home/user/myProgram')
k.executeProgram('Home/user/myProgram1')
k.executeProgram('Home/user/myProgram2')
k.executeProgram('Home/user/myProgram3')


