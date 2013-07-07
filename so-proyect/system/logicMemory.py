'''
Created on 07/06/2013

@author: Jose
'''

from hardware import PhysicalMemory
import instructions as i
import processAndProgram as p
import interruptions as ii
import kernel
import Queue as q
import hardware
from interruptions import PageFaultContext 


from processAndProgram import PCB

import instructions as i
import processAndProgram as p
import random


"""**********Logic Memory***********"""
"""Super clase de asignacion continua y paginacion"""
class LogicMemory():
    
    def __init__(self,disk,physicalMemory):
        self.disk=disk
        self.physicalMemory=physicalMemory
        
    def allocateInstructionInMemoryPhysical(self,instruction,elementOfMemory):
        direction=elementOfMemory.directionPhysical
        for ins in instruction:
            self.physicalMemory.setData(direction,ins)
            direction+=1

"""**********ASIGNACION CONTINUA***********"""

    
class ContinuousAssignment(LogicMemory):
    
    def __init__(self, disk, physicalMemory,setting,plp=None):
        self.plp=plp
        self.disk = disk
        self.physicalMemory = physicalMemory
        self.freeBlocks=self.generateFreeBlock(physicalMemory)
        self.setting = setting
        self.takenBlock={}#es un diccionario,la clave es el pcb y el valor un bloque asignado
     
    """parte el bloque(si es mas grande que el pcb)y se lo asigna al pcb ,tambien guarda las
       instrucciones en la memoria fisica
    """    
    def allocate(self, pcb, block,instructions,size):

        if(not block.entersJustBlock(size)):
            self.takenBlock[pcb]=block.breakBlock(size)
        else:
            self.takenBlock[pcb]=block
            self.deleteBlockFree(block)
        self.allocateInstructionInMemoryPhysical(instructions,self.takenBlock[pcb])    
    
    
    def isBlockFree(self,aBlock):

        for block in self.freeBlocks:
            if(block == aBlock):
                return True
        return False
    
    def deleteBlockFree(self,aBlock):

        if(self.isBlockFree(aBlock)):
            self.freeBlocks.remove(aBlock)
    
    """dado una size compacta la memoria logica y retorna el bloque de tamanho size 
       Tambien mueve todas las bloques de instrucciones de la memoria fisica
    """
    def compactTo(self,size):
        sizeAll=self.getFreeSpace()
        
        newBlock=Block(sizeAll,0)
        self.moveBlocks(sizeAll)
        self.freeBlocks=[newBlock]
        if newBlock.entersBlock(size):
            if newBlock.entersJustBlock(size):
                return newBlock
            else:
                return newBlock.breakBlock(size)
    
    """
    dado una direccion inicial,mueve todos los bloques tomados los los pcb empezando por la
    direccion inicial(memoria fisica y logica)
    """
    def moveBlocks(self,directinoIni):

        dir=directinoIni
        taken=self.takenBlock.values()
        for block in taken:
            instructions=self.getInstructions(block)
            block.directionPhysical=dir
            self.allocateInstructionInMemoryPhysical(instructions,block)
            dir+=block.size
    
    """
    Dado un bloque retorna todas las instrucciones almacenadas en memoria fisica
    """  
    def getInstructions(self,block):

        directionPhysical=block.directionPhysical
        listIns=[]
        for i in range(block.size):
            listIns.append(self.physicalMemory.getData(directionPhysical))
            directionPhysical+=1
        return listIns
        
         
    def fetchInstruction(self,pcb):
        instruction=self.physicalMemory.getData(self.takenBlock[pcb].directionPhysical + pcb.pc)
        pcb.addPc()
        return instruction
            
    
    """dado el tamanho de memoria fisica generia un block free""" 
    def generateFreeBlock(self,physicalMemory):

        return [Block(physicalMemory.getSize(),0)]
    
     
    def allocateMemory(self,pcb):
        """Obtiene un bloque de disco ,que almacena las instrucciones del pcb"""
        dblock=self.disk.getDiskBlock(pcb)
        size=pcb.size

        """ delega al ajuste la buqueda de un bloque de tamanho size,puede no encotrarlo,en ese caso
            retorna none
        """
        block=self.setting.getFreeBlockTo(size,self.freeBlocks)
        
        """si el bloque es none,se debe compactar,caso contrario ya se puede guardar en memoria"""
        if(block is None):
            """si se compacta  y se guarda el pcb en el bloque compactado
            """
            block=self.compactTo(size)
            self.allocate(pcb, block,dblock.getInstructions(),size)
            
        else:

            self.allocate(pcb, block,dblock.getInstructions(),size)
      
      
    def getFreeSpace(self):
        size=0
        for block in self.freeBlocks:
            size+=block.size       
        return size
    
    def freeSpaceInMemory(self,size):
        return self.getFreeSpace()>=size
    
    def freeSpaceInDisk(self,size):
        return True
     
    """Libera la memoria usada por el pcb"""   
    def kill(self,pcb):
        i=self.takenBlock.keys()
        res=False
        for n in i:
            if(n == pcb):
                res=True
        if(not res):
            return
        block=self.takenBlock[pcb]
        del(self.takenBlock[pcb])
        self.freeBlocks.append(block)
        self.plp.notify(pcb.size)
        
    def show(self):
        pq=q.PriorityQueue()
        for block in self.takenBlock.values():
            pq.put((block.directionPhysical,block,))
        for block in self.freeBlocks:
            pq.put((block.directionPhysical,block,))
        print 'ocupado :',len(self.takenBlock.values())
        print 'free:',len(self.freeBlocks)
        while not pq.empty():    
            o=pq.get()
            ini=o[0]
            """"""
            d=None
            for k in self.takenBlock.keys():
                if(self.takenBlock[k]==o[1]):
                    d=k
            mitad=o[1].size/2   
                    
            """"""
            print '+------------------------+'
            for i in range(o[1].size):
                if(mitad == i):
                    if(d is not None):
                        print '/        ',d.pid,'             / ' ,ini
                    else:
                        print '/        free            / ' ,ini
                else:
                    print '/                        / ' ,ini
                ini+=1
        print '+------------------------+' 
 
 
"""Bloques de para asignacion continua y frames para paginacion""" 

class ElementOfMemory():
    
    def __init__(self,directionPhysical):
        """esta direccion hace referencia a una direccion de memoria fisica"""
        self.directionPhysical=directionPhysical
        
class Block(ElementOfMemory):
    def __init__(self,size,directionPhysical):
        self.size= size
        ElementOfMemory.__init__(self,directionPhysical)
    
    """dado otro block retorna uno nuevo compactado"""
    def compact(self,otherBlock):

        return Block(self.size+otherBlock.size,self.directionPhysical)
   

    def entersBlock(self,size):

        return  size <= self.size
    
    def entersJustBlock(self,size):

        return  size == self.size
    
    def isHigher(self,otherBlock):

        return self.size >= otherBlock.size
    
    def breakBlock(self,size):
        self.size-=size
        block=Block(size,self.size+self.directionPhysical)
        return block

        
    
class Frame(ElementOfMemory):
    
    def __init__(self,directionLogic,directionPhysical):
        self.directionLogic=directionLogic
        ElementOfMemory.__init__(self,directionPhysical)

    def getInstruction(self,pcb,physicalMemory,resto):
        pcb.addPc()
        return physicalMemory.getData(self.directionPhysical+resto)
  
  
"""ALGORITMOS DE BUSQUEDA DE BLOCKES"""  
        
class Setting():
    
    def getFreeBlockTo(self,size,freeBloc):
        pass

class FirstFit(Setting):
    
    def getFreeBlockTo(self, size, freeBloc):
        for block in freeBloc:
            if(block.entersBlock(size)):
                return block
        return None
    
class BestFit(Setting):
    
    def getFreeBlockTo(self, size, freeBloc):
        for block in freeBloc:
            if(block.entersJustBlock(block)):
                return block
        return None
    
class WorstFit(Setting):
    
    def getFreeBlockTo(self, size, freeBlock):
        if len(freeBlock)==0:
            return None
        blockMax=freeBlock[0]
        for block in freeBlock:
            if(not blockMax.isHigher(block)):
                blockMax=block
        if(blockMax.entersBlock(size)):
            return blockMax
        return None
    


        
"""***********PAGINACION***************"""

class Page():
    
    def __init__(self,direction):
        self.direction=direction
        self.isDisk=False
        self.isMemory=False
        


class Paging(LogicMemory):
    
    def __init__(self, disk, physicalMemory,replacementAlgorithms,plp=None):
        self.plp=plp
        self.disk = disk
        self.physicalMemory = physicalMemory
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
    def fetchInstruction(self,pcb): 
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
       

            
    """Actualiza la tabla de pagina de pcb"""
    def updateTablePageOf(self,pcb,page,frame):
        self.pagesOfPcb[pcb].updateTablePage(page,frame)

    
    
    """obtiene y retorna todas las instrucciones del frame almacenadas en memotia fisica"""
    def getDataOfPhysical(self,frame):
        ins=[]
        direction=frame.directionPhysical
        for dir in range(self.sizePage):
            ins.append(self.physicalMemory.getData(direction))
            direction+=1
        return ins
    
    def freeSpaceInMemory(self,size):
        return True
    
    def freeSpaceInDisk(self,size):
        return self.disk.getFreeSwapSpace() >= size
    
    def kill(self,pcb):
        """libera los frames usados por el pcb,tambien las pages que mantiene el algoritmo de lemplazo
           
        """
        self.disk.removePcbInSwap(pcb.pid)
        usedFrame=self.pagesOfPcb[pcb].getUsedFrames(self.frames)
        self.replacementAlgorithms.removePages(self.pagesOfPcb[pcb].pages)
        del self.pagesOfPcb[pcb]
        for frame in usedFrame:
            self.takenFrame.remove(frame)
        self.plp.notify(pcb)
            
      
"""Esta clase contiene una lista de paginas y una tabla de paginas"""   
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
            ii.ManagerInterruptions.throwInterruption(ii.Interruption.pageFault,PageFaultContext(pcb,page))
    
    

       
    def updateTablePage(self,page,frame):
        self.tablePages[page.direction]=frame.directionLogic 
        
    def getFrameOf(self,page):
        return self.tablePages[page.direction]  
    
    def getUsedFrames(self,frames):
        nsframes=self.tablePages.values()
        fs=[]
        for nframe in nsframes:
            fs.append(frames[nframe])
        return fs
    
    



"""algoritmos de remplazos de paginas"""
class ReplacementAlgorithms():
    
    def __init__(self,paging=None):
        self.queue=q.Queue()
        self.takenPage={}
        self.paging=paging
    
    
    def removePages(self,pages):
        for page in pages:
            del(self.takenPage[page])
            
    def getFrame(self,page,pagesOfPcb,kernel):
        pcb=self.takenPage[page]
        pageData=pagesOfPcb[pcb]
        page.isMemory=False
        nframe=pageData.getFrameOf(page)
        frame=self.paging.frames[nframe]
        kernel.swapOut(page,pcb,frame)
        return frame
        
        
    
   

class FIFO(ReplacementAlgorithms):    
     
    def __init__(self,paging=None):
        ReplacementAlgorithms.__init__(self,paging)
        
     
    def register(self,page,pcb):
        self.takenPage[page]=pcb
        self.queue.put(page)
        
    def getFrame(self,pagesOfPcb,kernel):
        page=self.queue.get()
        return ReplacementAlgorithms.getFrame(self,page,pagesOfPcb,kernel)

    def removePages(self,pages):
        ReplacementAlgorithms.removePages(self, pages)
        newQueue=q.Queue()
        while not self.queue.empty():
            page=self.queue.get()
            if(not page in pages):
                newQueue.put(page)
        self.queue=newQueue
        
        
class NotRecentlyUsed():
    
    def __init__(self,paging=None):
        ReplacementAlgorithms.__init__(self,paging)
    
    """Chekea todos los flags asociados a las paginas,si encuentra page con flag en true,retorna esa,
       si no le cambia el flag a True y lo vuelve a meter en la cola 
    """
    def getFrame(self,pagesOfPcb,kernel):
        tupla=self.queue.get()
        
        while(not tupla[1]):
            tupla[1]=True
            self.queue.put(tupla)
            tupla=self.queue.get()
            
            
        page=tupla[0]
        return ReplacementAlgorithms.getFrame(self,page,pagesOfPcb,kernel) 
        
    
    def register(self,page,pcb):  
        self.takenPage[page]=pcb
        self.queue.put([page,False])

    def removePages(self,pages):
        ReplacementAlgorithms.removePages(self, pages)
        newQueue=q.Queue()
        while(not self.queue.empty()):
            page=self.queue.get()[0]
            if(page not in pages):
                newQueue.put(page)
        self.queue=newQueue
            
            
                
                