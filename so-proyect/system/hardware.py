'''
Created on 08/04/2013

@author: Di Meglio
'''


class Memory():
    def __init__(self,size=256):
        self.rows=range(size);
        self.size=size
            
    def getData(self,position):
        return self.rows[position]
    
    def setData(self,position,data):
        self.rows[position]=data
            



