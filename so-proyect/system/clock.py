'''
Created on 13/05/2013

@author: Di Meglio
'''
import threading  as t
import time
from interruptions  import Interruption 

class Clock(t.thread):
    
    def _init_(self,cpu,timer,managerInterruption):
        self.cpu=cpu;
        self.timer=timer
        self.managerInterruption=managerInterruption
    
    def run(self):
        while(True):
            time.sleep(1)
            self.timer.click(self.cpu,self.managerInterruption)
            
            
class TimerQuantum():
    
    def _init_(self,quantum):
        self.quantum=quantum
        self.currentTime=0
        
    def click(self,cpu,managerInterruption):
        if(self.quantum>self.currentTime):
            cpu.click()
            self.currentTime+=1
        else:
            self.currentTime=0
            managerInterruption.throwInterruption(Interruption.timeOut)
        
        
        
class Timer():
        
    def click(self,cpu):
        cpu.click()
    