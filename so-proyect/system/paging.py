'''
Created on 07/06/2013

@author: Nose
'''
from hardware import MMU
from hardware import PhysicalMemory

class Page():
    
    def __init__(self,dir):
        self.dir=dir
        
    def getDirection(self,sizePage):
        return self.dir+ sizePage
        
        

class Paging(MMU):
    
    def __init__(self, disk, physicalMemory,replacementAlgorithms):
        MMU.__init__(self,disk,physicalMemory)
        self.freePage=self.generatePages(physicalMemory.getSize())
        self.takenPages=[]
        self.sizePage=4
        self.replacementAlgorithms=replacementAlgorithms
 
    def generatePages(self,sizeMemory):
        pages=[]
        for i in range (0, sizeMemory):
            pages.append(Page(i*(self.sizePage)))
        return pages
      
    def allocateMemory(self, pcb):
        instructions=self.disk.getInstructions(pcb)   
        pages=self.getPagesTo(instructions)
        self.takenPages[pcb]=pages
    
    
    def getInstruction(self, pcb):
        page=self.getPage(pcb)
        direction=page.getDirection(pcb.pc % self.sizePage,self.sizePage)
        return self.physicalMemory[direction]
         
    def getPage(self,pcb):
        pass
   
    def getPagesTo(self,instructions):
        size=len(instructions)
        if(size <= self.freePage):
            pages=[]
            for i in range(1,size):
                pages.append(self.freePage[i])
                del(self.freePage[i])
            return pages
        else:
            return self.replacementAlgorithms.getPages(self.disk,self)
   
   
    def getAmountPages(self,size):
        if(size%self.sizePage == 0):
            return size/self.sizePage
        else:
            return size/self.sizePage+1
   
    

class ReplacementAlgorithms():
    
    def getPages(self,disk,paging):
        pass
        

class FIFO(ReplacementAlgorithms):    
    pass


class NotRecentlyUsed():
    pass

"""     
p=Paging('',PhysicalMemory())
print len(p.freePage)
"""
