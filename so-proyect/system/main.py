'''
Created on 24/05/2013

@author: Di Meglio
'''
import threading  as t
import kernel
import cpu
import scheduler
import hardware
import process
import instructions as i 
import time
import random


class agregar(t.Thread):
    
    def __init__(self,kernel,pos):
        t.Thread.__init__(self) 
        self.kernel=kernel
        self.pos=pos
    
    def run(self):
#         time.sleep(random.randrange(0,3))
        self.kernel.memory.setData(self.pos,i.Cpu())
        self.kernel.memory.setData(self.pos+1,i.Cpu())
        self.kernel.memory.setData(self.pos+2,i.Cpu())
        self.kernel.memory.setData(self.pos+3,i.Cpu())
        self.kernel.memory.setData(self.pos+4,i.Cpu())
        self.kernel.memory.setData(self.pos+5,i.Finalize())
        self.kernel.addPcb(process.PCB(0, 0, self.pos,self.pos,self.pos))




memory=hardware.Memory(1500)
mode=kernel.Mode()

kernel=kernel.Kernel(cpu.CPU(memory,mode),memory,scheduler.RoundRobin(False),'disk',mode)
kernel.start()


for n in range(200):
    a=agregar(kernel,n*6)
    a.start()
    


while not kernel.scheduler.policy.isEmpty():
    time.sleep(4)
    print 'vacia:',kernel.scheduler.policy.isEmpty()
    print 'size:',len(kernel.scheduler.policy.processes.elements)




