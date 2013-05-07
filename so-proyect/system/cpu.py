'''
Created on 29/04/2013

@author: Di Meglio
'''

import scheduler

class CPU():
    
    def __init__(self,kernel):
        self.kernel=kernel
        

        
    def click(self):
        process=self.kernel.getPorcess()
        process.getInstruction().execute()