'''
Created on 07/06/2013

@author: Nose
'''
from hardware import MMU
from hardware import PhysicalMemory
import instructions as i
import process as p

class Page():
    
    def __init__(self,dir):
        self.dir=dir
        self.pidCurrent=None
        
    def getDirection(self,sizePage):
        return self.dir+ sizePage
        
        

class Paging(MMU):
    
    def __init__(self, disk, physicalMemory,replacementAlgorithms):
        MMU.__init__(self,disk,physicalMemory)
        self.takenPages={}
        self.sizePage=8
        self.replacementAlgorithms=replacementAlgorithms
        self.freePage=self.generatePages(physicalMemory.getSize())
 
    """genera sizeMemory paginas,cada una con su direccion"""
    def generatePages(self,sizeMemory):
        pages=[]
        for i in range (0, sizeMemory):
            pages.append(Page(i*(self.sizePage)))
        return pages
      
    """ guarda en memoria fisica las instrucciones del pcb"""
    def allocateMemory(self, pcb):
        instructions=self.disk.getInstructions(pcb)   
        pages=self.getPagesTo(len(instructions),pcb)
        self.takenPages[pcb]=pages
        
    
    """ busca en memoria fisica la instruccion del pcb segun su pc"""
    def getInstruction(self, pcb):
        page=self.getPage(pcb)
        direction=page.getDirection(pcb.pc % self.sizePage,self.sizePage)
        return self.physicalMemory[direction]
         
    """retorna la pagina la cual necesita el pcb para buscar la instruccion,
       si no tiene pagina busca una en disco
     """
    def getPage(self,pcb):
        npage=pcb.pc / self.physicalMemory.getSize()
        if(self.takenPages[pcb][npage].pidCurrent == pcb.pid):
            return self.takenPages[pcb][npage]
        else:
            interruptionsManager.page=self.takenPages[pcb][npage]
            interruptionsManager.trwosInterruption(Interruption.pages)
            self.takenPages[pcb][npage]
            
        
        if(len(self.takenPages[pcb]) <npage):
            instructions=self.disk.getInstructions(pcb)
            pages=self.getPagesTo(len(instructions), pcb)
            self.loadedIntoMemory(pages,instructions)
            self.AddAll(self.takenPages[pcb],pages)
            return self.takenPages[pcb][npage]
        else:
            return self.takenPages[pcb][npage]
            
        
    """ retorna todas las pagias que necesita el pcb ,si no hay suficiente,las busca en disco"""
    def getPagesTo(self,sizeIntructions,pcb):
        size=self.getAmountPages(sizeIntructions)
        current=0
        pages=[]
        while(size> current and len(self.freePage)>0):
            pages.append(self.freePage[current])
            del(self.freePage[current])
            current+=1
     
        if(len(pages) < size):
            pagesRest=self.replacementAlgorithms.getPages(self.disk,self,len(pages)-size-self.AmountPagesPcb(pcb))
            self.AddAll(pages, pagesRest)
        
        return pages
       
    """ a las paginas pagesA agrega pagesB"""
    def AddAll(self,pagesA,pagesB):
        for page in pagesB:
                pagesA.append(page) 
   
   
    """retorna la cantidad de pages que necesitan las instrucciones de tamanho size"""
    def getAmountPages(self,size):
        if(size%self.sizePage == 0):
            return size/self.sizePage
        else:
            return size/self.sizePage+1
   
    """retorna la cantidad de pages que tiene el pcb"""
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




class Disk():
    
    def getInstructions(self,pcb):
        a=i.Cpu()
        b=i.Cpu()
        c=i.Cpu()
        d=i.Cpu()
        e=i.Cpu()
        f=i.Cpu()
        g=i.Cpu()
        h=i.Cpu()
        list=[a,b,c,d,a,b,c,d,e,a,b,c,d,a,b,c,d,a,b,c,d]
        return list
    

    
pa=Paging(Disk(),PhysicalMemory(),'')
ppp=p.PCB(0,0,0,0,0)
pa.allocateMemory(ppp)


for i in pa.takenPages[ppp]:
    print i.dir
    
print len(pa.freePage)





