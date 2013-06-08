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
        self.takenPages=[]
        self.sizePage=8
        self.replacementAlgorithms=replacementAlgorithms
        self.freePage=self.generatePages(physicalMemory.getSize())
 
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
        if(len(self.takenPages[pcb]) <npage):
            instructions=self.disk.getInstructions(pcb)
            pages=self.getPagesTo(len(instructions), pcb)
            self.loadedIntoMemory(pages,instructions)
            self.AddAll(self.takenPages[pcb],pages)
            return self.takenPages[pcb][npage]
        else:
            return self.takenPages[pcb][npage]
            
        
   
    def getPagesTo(self,sizeIntructions,pcb):
        size=self.getAmountPages(sizeIntructions)
        current=0
        while(size> current & len(self.freePage)>0):
            pages=[]
            pages.append(self.freePage[current])
            del(self.freePage[current])
            
        if(len(pages) < size):
            pagesRest=self.replacementAlgorithms.getPages(self.disk,self,len(pages)-size-self.AmountPagesPcb(pcb))
            self.AddAll(pages, pagesRest)
        
        return pages
       
    def AddAll(self,pagesA,pagesB):
        for page in pagesB:
                pagesA.append(page) 
   
   
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




