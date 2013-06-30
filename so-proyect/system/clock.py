'''
Created on 13/05/2013

@author: Di Meglio
'''
import threading  as t
import time
from interruptions  import Interruption 
import interruptions as i


class Clock(t.Thread):
    
    def _init_(self,cpu,timer):
        t.Thread.__init__(self)
        self.cpu=cpu;
        self.timer=timer
    
    def run(self):
        while(True):
            time.sleep(1)
            self.timer.click(self.cpu)
            print 'tiempo de cpu'
 
class Timer():
        
    def click(self,cpu):
        cpu.click()  
        
    def resetQuantum(self):
        pass        
            
class TimerQuantum(Timer):
    
    def __init__(self,quantum):
        self.quantum=quantum
        self.currentTime=0
        
    def click(self,cpu):
        if(self.quantum>self.currentTime):
            Timer.click(self,cpu)
            self.currentTime+=1
        else:
            self.resetQuantum()
            i.ManagerInterruptions.throwInterruption(Interruption.timeOut,None)
            
    def resetQuantum(self):
        self.currentTime=0
        
        
        

    