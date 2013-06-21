'''
Created on 07/06/2013

@author: Nose
'''
from hardware import MMU
from hardware import PhysicalMemory
import instructions as i
import process as p
import interruptions as ii
import kernel

class Page():
    
    def __init__(self):
        self.isDisk=False
        self.isMemory=False
        
        
# direction=page.getDirection(pcb.pc % self.sizePage,self.sizePage)

class Paging(MMU):
    
    def __init__(self, disk, physicalMemory,replacementAlgorithms):
        MMU.__init__(self,disk,physicalMemory)
        self.takenFrames={}
        self.sizePage=8
        self.replacementAlgorithms=replacementAlgorithms
        self.frames=self.generateFrames(physicalMemory.getSize())
 
    """genera sizeMemory paginas,cada una con su direccion"""
    def generateFrames(self,sizeMemory):
        frames=[]
        for i in range (0, sizeMemory):
            frames.append(Frame(i*(self.sizePage)))
        return frames
      
    """ guarda en memoria fisica las instrucciones del pcb"""
    def allocateMemory(self, pcb):   
        pages=self.getPagesTo(pcb.size)
        self.takenFrames[pcb]=PageData(pages)
        
            
        
    """ retorna todas las pagias que necesita el pcb ,si no hay suficiente,las busca en disco"""
    def getPagesTo(self,size):
        amount=self.getAmountPages(size)
        pages=[]
        for i in range(amount):
            pages.append(Page())
        return pages
            
    def getInstruction(self,nframe,pcb):
        frame=self.frames[nframe]   
        return frame.getInstruction(pcb,self.physicalMemory)
   
   
    """retorna la cantidad de pages que necesitan las instrucciones de tamanho size"""
    def getAmountPages(self,size):
        if(size%self.sizePage == 0):
            return size/self.sizePage
        else:
            return size/self.sizePage+1
       
       
    def getData(self,pcb): 
        return self.takenFrames[pcb].getInstruction(pcb,self.physicalMemory,self)
        
             
    def getFrame(self):
        if(len(self.replacementAlgorithms.queue)!=0):   
            return self.replacementAlgorithms.getFrame(self.takenFrames)
        else:
            return self.getFreeFrame()
        
        
     
   

    
    
      
      
class PageData():
    
    def __init__(self,pages):
        self.pages=pages
        self.TablePages= {}   
        
    def getInstruction(self,pcb,physicalMemory,paging):
        npage=pcb.pc / physicalMemory.getSize()
        page=self.pages[npage]  
        if(page.isMemory):
            nframe=self.TablePages[page.direction]
            return paging.getInstruction(nframe,pcb)
        elif(page.isDisk):
            ii.ManagerInterruptions.throwInterruption(ii.Interruption.pageFaultInDisk)
        else:
            ii.ManagerInterruptions.paging=paging
            ii.ManagerInterruptions.pcb=pcb
            ii.ManagerInterruptions.throwInterruption(ii.Interruption.pageFault)
      
    def allocateInMemoryPhysical(self,pcb,frame): 
        iss=self.disk.getInstructions(pcb)
        dir=frame.direction
        for i in iss:
            self.physicalMemory.setData(dir,i)
            dir+=1
             
         

class Frame():
    
    def __init__(self,direction):
        self.direction=direction




"""algoritmos de remplazos de paginas"""
class ReplacementAlgorithms():
    
    def getPages(self,disk,paging):
        pass
        

class FIFO(ReplacementAlgorithms):    
     
    def __init__(self):
        self.queue=[]
        self.takenBlock={}
     
     
    def register(self,block,pcb):
        self.takenBlock[block]=pcb
        self.queue.append(block)
        
    def getFrame(self,takenBlock):
        block=self.queue[0]
        del self.queue[0]
        dataPage=takenBlock[self.takenBlock[block]]
        page=dataPage.getPageOf(block)
        return {'page':page,'block':block} 

    def free(self,block):
        del self.takenBlock[block]
        self.queue.remove(block)
        
        
class NotRecentlyUsed():
    
    def register(self,block,pcb):
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
        list=[a,b,c,d,a]
        return list
    
ii.ManagerInterruptions.config(None, kernel.Mode(), None,None)
    
pa=Paging(Disk(),PhysicalMemory(),FIFO())
p=p.PCB(0,0,0,4,0)
pa.allocateMemory(p)

"""
for i in pa.takenPages[ppp]:
    print i.dir
    
print len(pa.freePage)
"""
print pa.takenFrames[p].pages
pa.getData(p)


