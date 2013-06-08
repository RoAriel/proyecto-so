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
        pages=self.getPagesTo(len(instructions),pcb)
        self.takenPages[pcb]=pages
    
    
    def getInstruction(self, pcb):
        page=self.getPage(pcb)
        direction=page.getDirection(pcb.pc % self.sizePage,self.sizePage)
        return self.physicalMemory[direction]
         
    def getPage(self,pcb):
        npage=pcb.pc / self.physicalMemory.getSize()
        self.takenPages[pcb][npage]
        return self
   
    def getPagesTo(self,sizeIntructions,pcb):
        size=self.getAmountPages(sizeIntructions)
        current=0
        while(size> current & len(self.freePage)>0):
            pages=[]
            pages.append(self.freePage[current])
            del(self.freePage[current])
            
        if(len(pages) < size):
            pagesRest=self.replacementAlgorithms.getPages(self.disk,self,len(pages)-size-self.AmountPagesPcb(pcb))
            for page in pagesRest:
                pages.append(page)
        
        return pages
        
   
   
    def getAmountPages(self,size):
        if(size%self.sizePage == 0):
            return size/self.sizePage
        else:
            return size/self.sizePage+1
   
    def AmountPagesPcb(self,pcb):
        return len(self.takenPages[pcb])
    
                



"""algoritmos de remplazos de paginas"""
class ReplacementAlgorithms():
    
    def getPages(self,disk,paging):
        pass
        

class FIFO(ReplacementAlgorithms):    
    pass


class NotRecentlyUsed():
    pass




class Kernel():
    
    def __init__(self):
        self.abc=2
        
    def a(self):
        print self.abc
    

    
p=Paging('',PhysicalMemory(),'')


r=Kernel()
r.a()