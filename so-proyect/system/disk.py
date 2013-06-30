'''
Created on 24/06/2013

@author: usuario
'''
from process import PCB


class Disk():
    
    def __init__(self,sizeBlock):
        self.sizeBlock=sizeBlock
        self.programs={}
        self.runPrograms={}

        
    def addProgram(self,programa,pid):
        size=programa.size()
        instructions=programa.getInstructions()
        amountBlock=self.getAmountBlock(size)
        number=0
        blocks=[]
        bool=False
        for i in range(amountBlock):
            list=[]
            for n in range(self.sizeBlock):
                if(number != len(instructions)):
                    
                    list.append(instructions[number])
                    number+=1
                else:
                    self.programs[pid]=blocks
                    bool=True
                    break
            blocks.append(DiskBlock(list))
            if bool:
                break
        self.programs[pid]=blocks
                
                
    def getBlock(self,page,pid):
        return self.programs[pid][page.direction]
    
        
    def getAmountBlock(self,size):
        if(size % self.sizeBlock == 0):
            return size/self.sizeBlock
        else:
            return size/self.sizeBlock+1
        
        
    def execute(self,pathProgram):
        pcb=PCB(PidGenerator.getPid(),0,0)
        self.kernel.addPcb(pcb)
        self.runPrograms[pathProgram].append(pcb.pid)
    

    
    
class DiskBlock():
    
    def __init__(self,instructions):
        self.instructions=instructions
    
    def getInstructions(self):
        return self.instructions
    

class PidGenerator():
    
    def __init__(self):
        self.inital=0
     
    @classmethod      
    def getPid(self):
        pid=self.inital
        self.inital+=1
        return self.pid
