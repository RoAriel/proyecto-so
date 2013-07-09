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
Se crea un kernel con policy FCFS,sistema de asignacion continua(usando el algoritmo BestFit)

"""
"""Estas variables de pueden configurar a gusto,ejemplo: se puede elegir otro scheduler"""
mode=kernel.Mode()
physicalMemory=hardware.PhysicalMemory(16)
disk=hardware.Disk(8)
acont=logicMemory.ContinuousAssignment(disk, physicalMemory,logicMemory.BestFit())
cpu=CPU(acont,mode)
scheduler=scheduler.FCFS()


k=kernel.Kernel(cpu,physicalMemory,acont,scheduler,disk,mode)
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

acont.show()

"""se ejecutan los programas y se muestra la memoria"""
k.executeProgram('Home/user/myProgram2')
k.executeProgram('Home/user/myProgram2')
k.executeProgram('Home/user/myProgram3')

k.showReedyProcess()
"""mustra la memoria despues de guardar los procesos ejecutados,
   se puede ver solo hay un bloque libre
"""
acont.show()


"""se espera a que finalizen todos los procesos,se ejecuta nuevamente un programa
   como no hay bloques de su tamaho se debe compactar la memoria
"""
time.sleep(21)
k.memoryLogic.show()
k.executeProgram('Home/user/myProgram')

"""Ahora mostraria la memoria compactada y con el proceso del programa ejecutado arriba"""
k.memoryLogic.show()

time.sleep(12)
k.stop()
