'''
Created on 24/05/2013

@author: j di meglio
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
Se crea un kernel con policy RoundRobin(Sin prioridad y quantum 2),sistema de asignacion continua(usando el algoritmo FirstFit)

"""

mode=kernel.Mode()
physicalMemory=hardware.PhysicalMemory(16)
disk=hardware.Disk(8)
acont=logicMemory.ContinuousAssignment(disk, physicalMemory,logicMemory.BestFit())
cpu=CPU(acont,mode)
scheduler=scheduler.RoundRobin(False,2)


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

"""Se puede ver el estado inicial de memoria,un bloque de tamanho de memoria fisica"""
acont.show()

"""se ejecutan los programas y se muestra la memoria"""
k.executeProgram('Home/user/myProgram2')
k.executeProgram('Home/user/myProgram2')
k.executeProgram('Home/user/myProgram3')


"""mustra la memoria despues de guardar los procesos ejecutados,
   se puede ver solo hay un bloque libre
"""
acont.show()


"""se espera 15 segundos,solo un proceso termino,por lo tanto cunado se quiere ejecutar
   el programa  no hay espacio,entonces el plp lo pone en cola de wait,hasta que algun proceso
   muera ,es ahi cuando se empiza a ejecutar
"""
time.sleep(15)
k.memoryLogic.show()
k.executeProgram('Home/user/myProgram')

"""La memoria sigue igual,por que el proceso no pudo ser guardado,debido a que no hay suficiente
   tamanho en memoria
"""
k.memoryLogic.show()

