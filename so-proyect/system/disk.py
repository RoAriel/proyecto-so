'''
Created on 24/06/2013

@author: usuario
'''

class Disk():
    
    def __init__(self,sizeBlock):
        self.sizeBlock=sizeBlock
        self.programs={}

        
    def addProgram(self,programa,pid):
        size=programa.size()
        instructions=programa.getIntructions()
        amountBlock=self.getAmountBlock(size)
        number=0
        blocks=[]
        for i in range(amountBlock):
            for n in range(self.sizeBlock):
                if(number != len(instructions)):
                    list=[]
                    list.append(instructions[number])
                    number+=1
                else:
                    self.programs[pid]=blocks
                    return
            blocks.append(DiskBlock(list))
        self.programs[pid]=blocks
                
        
    def getAmountBlock(self,size):
        if(size%self.sizeBLock == 0):
            return size/self.sizeBlock
        else:
            return size/self.sizeBlock+1
        
        
    def ejecutar(self,pid):
        pass
    
    def swapOut(self):
        pass
    
    def swapIn(self):
        pass
    
    
class DiskBlock():
    
    def __init__(self,instructions):
        self.instructions=instructions
    
    
    
