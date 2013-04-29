'''
Created on 29/04/2013

@author: Di Meglio
'''

import scheduler

class CPU():
    
    def __init__(self,scheduler):
        self.scheduler=scheduler
        
    def run(self):
        while(True):
            process=self.scheduler.get()