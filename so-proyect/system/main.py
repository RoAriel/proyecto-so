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


class agregar(t.Thread):
    
    def __init__(self,kernel,pos):
        t.Thread.__init__(self) 
        self.kernel=kernel
        self.pos=pos
    
    def run(self):
        self.kernel.memory.setData(self.pos-1,i.Cpu())
        self.kernel.memory.setData(self.pos,i.Finalize())
        self.kernel.addPcb(process.PCB(0, 0, 0,self.pos-1,self.pos))




memory=hardware.Memory(900)
mode=kernel.Mode()

kernel=kernel.Kernel(cpu.CPU(memory,mode),memory,scheduler.RoundRobin(True),'disk',mode)
kernel.start()


for n in range(2):
    a=agregar(kernel,n+2)
    a.start()

time.sleep(3)
a=agregar(kernel,3)
a.run()

while not kernel.scheduler.policy.isEmpty():
    time.sleep(4)
    print 'vacia:',kernel.scheduler.policy.isEmpty()
    print 'size:',len(kernel.scheduler.policy.processes.elements)



