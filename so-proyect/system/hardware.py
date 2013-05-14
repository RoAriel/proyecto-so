'''
Created on 08/04/2013

@author: Di Meglio
'''

import random

class Memory():
    def __init__(self,size=256):
        self.rows=[];
        self.size=size
        for _ in range(self.size):
            self.rows.append(random.randrange(0, 99999))
            
    def getData(self,position):
        return self.rows[position]
    
    def setData(self,position,data):
        self.rows[position]=data
            
a = Memory()
print a


