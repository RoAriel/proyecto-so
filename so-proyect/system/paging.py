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
import Queue as q
import disk

class Page():
    
    def __init__(self,direction):
        self.direction=direction
        self.isDisk=False
        self.isMemory=False
        
        
# direction=page.getDirection(pcb.pc % self.sizePage,self.sizePage)

class Paging(MMU):
    
    def __init__(self, disk, physicalMemory,replacementAlgorithms):
        MMU.__init__(self,disk,physicalMemory)
        self.pagesOfPcb={}
        self.sizePage=8
        self.replacementAlgorithms=replacementAlgorithms
        self.frames=self.generateFrames(physicalMemory.getSize())
        self.takenFrame=[]
        replacementAlgorithms.paging=self
        disk.paging=self
 
    """genera sizeMemory frames,cada una con su direccion fisica"""
    def generateFrames(self,sizeMemory):
        frames=[]
        directionLogic=0
        for i in range (0, sizeMemory/self.sizePage):
            frames.append(Frame(directionLogic,i*(self.sizePage)))
            directionLogic+=1
        return frames
      
    """ genera paginas necesarias para el pcb,sin cargarlas a memoria"""
    def allocateMemory(self, pcb):   
        pages=self.getPagesTo(pcb.size)
        self.pagesOfPcb[pcb]=PageData(pages)
        
            
        
    """ retorna todas las paginas que necesita el pcb """
    def getPagesTo(self,size):
        amount=self.getAmountPages(size)
        pages=[]
        direction=0
        for i in range(amount):
            pages.append(Page(direction))
            direction+=1
        return pages
            
    def getInstruction(self,nframe,pcb):
        frame=self.frames[nframe]   
        return frame.getInstruction(pcb,self.physicalMemory,pcb.pc % self.sizePage)
   
   
    """retorna la cantidad de pages que necesitan las instrucciones de tamanho size"""
    def getAmountPages(self,size):
        if(size%self.sizePage == 0):
            return size/self.sizePage
        else:
            return size/self.sizePage+1
       
    """retorna la instruccion que indique el pc del pcb"""   
    def getData(self,pcb): 
        npage=pcb.pc/self.sizePage
        return self.pagesOfPcb[pcb].getInstruction(pcb,npage,self.physicalMemory,self)
        
             
    def getFrame(self):
        """Si la cantidad de frame tomados es igual a la del total de frames
           no hay frame libres,tiene que ejecutar el algoritmo,caso contrario
           agarra un frame libre
        """
        if(len(self.takenFrame) == len(self.frames)):   
            return self.replacementAlgorithms.getFrame(self.pagesOfPcb,ii.ManagerInterruptions.kernel)
        else:
            frame= self.getFreeFrame()
            self.takenFrame.append(frame)
            return frame
    
    """
    retorna un frame libre 
    """
    def getFreeFrame(self):
        for frame in self.frames:
            if(not frame in self.takenFrame):
                return frame
       
    """dado un pcb carga en memoria las instrucciones""" 
    def allocateInMemoryPhysical(self,pcb,frame): 
        iss=self.disk.getInstructions(pcb)
        dir=frame.directionPhysical
        for i in iss:
            self.physicalMemory.setData(dir,i)
            dir+=1
     
    def updateTablePageOf(self,pcb,page,frame):
        self.pagesOfPcb[pcb].updateTablePage(page,frame)

    
    def allocateInstructionInMemoryPhysical(self,instruction,frame):
        direction=frame.directionPhysical
        for ins in instruction:
            self.physicalMemory.setData(direction,ins)
            direction+=1
    
    def getDataOfPhysical(self,frame):
        ins=[]
        direction=frame.directionPhysical
        for dir in range(self.sizePage):
            ins.append(self.physicalMemory.getData(direction))
            direction+=1
        return ins
    
    def kill(self,pcb):
        """libera los frames usados por el pcb,tambien las pages que mantiene el algoritmo de lemplazo
           y paginas almacenadas en disco
        """
        usedFrame=self.pagesOfPcb[pcb].getUsedFrames()
        self.pagesOfPcb[pcb].kill(self.replacementAlgorithms)
        del self.pagesOfPcb[pcb]
        for frame in usedFrame:
            self.takenFrame.remove(frame)
            
      
      
class PageData():
    
    def __init__(self,pages):
        self.pages=pages
        self.tablePages= {}   
        
    def getInstruction(self,pcb,npage,physicalMemory,paging):
        page=self.pages[npage]  
        if(page.isMemory):
            nframe=self.tablePages[page.direction]
            return paging.getInstruction(nframe,pcb)
        else:
            ii.ManagerInterruptions.paging=paging
            ii.ManagerInterruptions.pcb=pcb
            ii.ManagerInterruptions.page=page
            ii.ManagerInterruptions.throwInterruption(ii.Interruption.pageFault)
      
    def allocateInMemoryPhysical(self,pcb,frame): 
        iss=self.disk.getInstructions(pcb)
        dir=frame.direction
        for i in iss:
            self.physicalMemory.setData(dir,i)
            dir+=1
       
    def updateTablePage(self,page,frame):
        self.tablePages[page.direction]=frame.directionLogic 
        
    def getFrameOf(self,page):
        return self.tablePages[page.direction]  
    
    
    
    

class Frame():
    
    def __init__(self,directionLogic,directionPhysical):
        self.directionLogic=directionLogic
        self.directionPhysical=directionPhysical

    def getInstruction(self,pcb,physicalMemory,resto):
        return physicalMemory.getData(self.directionPhysical+resto)


"""algoritmos de remplazos de paginas"""
class ReplacementAlgorithms():
    
    pass

class FIFO(ReplacementAlgorithms):    
     
    def __init__(self,paging=None):
        self.queue=q.Queue()
        self.takenPage={}
        self.paging=paging
        
     
    def register(self,page,pcb):
        self.takenPage[page]=pcb
        self.queue.put(page)
        
    def getFrame(self,pagesOfPcb,kernel):
        page=self.queue.get()
        pcb=self.takenPage[page]
        pageData=pagesOfPcb[pcb]
        page.isMemory=False
        page.isDisk=True
        nframe=pageData.getFrameOf(page)
        frame=self.paging.frames[nframe]
        kernel.swapOut(page,pcb,frame)
        return frame

    def remove(self,page):
        pass
        
        
class NotRecentlyUsed():
    
    def __init__(self,paging=None):
        self.queue=q.Queue()
        self.takenPage={}
        self.paging=paging
    
    def getFrame(self,pagesOfPcb,kernel):
        tupla=self.queue.get()
        
        while(not tupla[1]):
            tupla[1]=True
            self.queue.put(tupla)
            tupla=self.queue.get()
            
            
        page=tupla[0]
        pcb=self.takenPage[page]
        pageData=pagesOfPcb[pcb]
        page.isMemory=False
        page.isDisk=True
        nframe=pageData.getFrameOf(page)
        frame=self.paging.frames[nframe]
        kernel.swapOut(page,pcb,frame)
        return frame  
        
                
        
    
      
    def register(self,page,pcb):  
        self.takenPage[page]=pcb
        self.queue.put([page,False])

    def remove(self,page):
        pass

"""***************************************************************************************"""
    

import hardware
import scheduler    
import cpu

memory=hardware.PhysicalMemory(8)
mode=kernel.Mode()


d=disk.Disk(8)
ii.ManagerInterruptions.disk=d
pa=Paging(d,memory,NotRecentlyUsed())
kernels=kernel.Kernel(cpu.CPU(pa,mode),memory,pa,scheduler.RoundRobin(False),d,mode)
    

ii.ManagerInterruptions.disk=d


import program 
pro=[]
for imp in range(5):
    p1=program.Program([i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Cpu(),i.Finalize()])
    d.addProgram(p1,imp)
    


proces=[]
for im in range(5):
    p1=p.PCB(0,0,im,10,im)
    pa.allocateMemory(p1)
    proces.append(p1)





for jj in range(10):
    cou=0
    # print len(pa.frames)
    while len(pa.pagesOfPcb.keys())>cou:
    #     print cou


        n= pa.getData(pa.pagesOfPcb.keys()[cou])
        print pa.pagesOfPcb.keys()[cou].pid
        print n
        if(n is not None):
#           n= pa.getData(pa.pagesOfPcb.keys()[cou])
            pa.pagesOfPcb.keys()[cou].addPc()
        else:
            n= pa.getData(pa.pagesOfPcb.keys()[cou])
            print n
            pa.pagesOfPcb.keys()[cou].addPc()
        cou+=1
        len(pa.pagesOfPcb.keys())>cou

    




