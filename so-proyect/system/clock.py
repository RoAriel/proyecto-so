'''
Created on 13/05/2013

@author: Di Meglio
'''
import threading  as t
import time

class Clock(t.thread):
    
    def _init_(self,cpu,timer):
        self.cpu=cpu;
        self.timer=timer
    
    def run(self):
        while(True):
            time.sleep(1)
            self.timer.click(self.cpu)
            
            
class TimerQuantum():
    
    def _init_(self,quantum):
        self.quantum=quantum
        self.currentTime=0
        
    def click(self,cpu):
        if(self.quantum>self.currentTime):
            cpu.click()
            self.currentTime+=1
        else:
            self.currentTime=0
            
        
        
        
class Timer():
        
    def click(self,cpu):
        cpu.click()
    