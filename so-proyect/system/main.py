'''
Created on 24/05/2013

@author: Di Meglio
'''

import kernel
import cpu
import scheduler
import hardware
import process
import instructions as i 
import time

memory=hardware.Memory()
mode=kernel.Mode()

kernel=kernel.Kernel(cpu.CPU(memory,mode),memory,scheduler.FCFS(),'disk',mode)
kernel.start()

time.sleep(5)
kernel.memory.setData(0,i.Finalize())
kernel.addPcb(process.PCB(0, 0, 0,0))

time.sleep(5)

print kernel.scheduler.policy.isEmpty()



