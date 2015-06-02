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

"""Se mustra la memoria lopgica,se puede ver un bloque libre de 16 espacios"""
acont.show()

k.executeProgram('Home/user/myProgram2')
k.executeProgram('Home/user/myProgram1')
k.executeProgram('Home/user/myProgram3')

"""ahora se puede ver 4 bloques,3 de ellos ocupados"""
acont.show()

time.sleep(15)

""""en este caso los procesos anteriores terminaron,se muestran los 4 bloques libres"""
acont.show()
k.executeProgram('Home/user/myProgram')

"""al ejecutar el ultimo programa de 11 instrucciones no hay bloque para ese tamanho,
   por lo tanto se debe compactar y guardar el proceso
"""
acont.show()

"""se puede ver el resultado de la ejecucion en el archivo info.log"""
"""Holaaaaa"""
