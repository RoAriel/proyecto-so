'''
Created on 13/05/2013

@author: Di Meglio
'''
import threading  as t
import time
from interruptions  import Interruption 
import interruptions as i
import logging

class Clock(t.Thread):
    
    def __init__(self,cpu,timer):
        t.Thread.__init__(self)
        self.cpu=cpu;
        self.timer=timer
        self.running=True
    
    def run(self):
        while(self.running):
            time.sleep(1)
            logging.info('****************************')
            logging.info('       TIEMPO DE CPU        ')
            self.timer.click(self.cpu)
            logging.info('****************************')
            
    def stop(self):
        self.running=False
 
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
        
        
        

    