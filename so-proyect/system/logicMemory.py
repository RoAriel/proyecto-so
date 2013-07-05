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

"""**********ASIGNACION CONTINUA***********"""
    
class ContinuousAssignment():
    
    def __init__(self, disk, physicalMemory,setting):

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
        self.allocateInMemoryPhysical(instructions,self.takenBlock[pcb])    
    
    
    def isBLockFree(self,aBlock):

        for block in self.freeBlocks:
            if(block == aBlock):
                return True
        return False
    
    def deleteBlockFree(self,aBlock):

        if(self.isBLockFree(aBlock)):
            self.freeBlocks.remove(aBlock)
    
    """dado una size compacta la memoria logica y retorna el bloque de tamanho size ,en el caso que retorne none
       quiere decir que no hay suficiente espacio para el pcb de tamanho size.
       Tambien mueve todas las instrucciones de la memoria fisica
    """
    def compactTo(self,size):


        sizeAll=0
        for block in self.freeBlocks:
            sizeAll+=block.size
            
        newBlock=Block(sizeAll,0)
        self.moveBlocks(sizeAll)
        self.freeBlocks=[newBlock]
        if newBlock.entersBlock(size):
            if newBlock.entersJustBlock(size):
                return newBlock
            else:
                return newBlock.breakBlock(size)
        return None
    
    """
    dado una direccion inicial,mueve todos los bloques tomados los los pcb empezando por la
    direccion inicial(memoria fisica y logica)
    """
    def moveBlocks(self,directinoIni):

        dir=directinoIni
        taken=self.takenBlock.values()
        for block in taken:
            instructions=self.getInstructions(block)
            block.direction=dir
            self.allocateInMemoryPhysical(instructions,block)
            dir+=block.size
    
    """
    Dado un bloque retorna todas las instrucciones almacenadas en memoria fisica
    """  
    def getInstructions(self,block):

        direction=block.direction
        listIns=[]
        for i in range(block.size):
            listIns.append(self.physicalMemory.getData(direction))
            direction+=1
        return listIns
         
    def fetchInstruction(self,pcb):
        return self.physicalMemory.getData(self.takenBlock[pcb].direction + pcb.pc)
            
    
    """dado el tamanho de memoria fisica generia un block free""" 
    def generateFreeBlock(self,physicalMemory):

        return [Block(physicalMemory.getSize(),0)]
    
     
    def allocateMemory(self,pcb):
        """Obtiene un bloque de disco ,que almacena las instrucciones del pcb"""
        dblock=self.disk.getDiskBlock(pcb)
        size=dblock.size()

        """ delega al ajuste la buqueda de un bloque de tamanho size,puede no encotrarlo,en ese caso
            retorna none
        """
        block=self.setting.getFreeBlockTo(size,self.freeBlocks)
        
        """si el bloque es none,se debe compactar,caso contrario ya se puede guardar en memoria"""
        if(block is None):
            """si se compacta  y block sigue siendo none,quiere decir que no hay espacio,el pcb no puede ser
               guardado en memoria en este momento
            """
            block=self.compactTo(size)
            if(block is not  None):

                self.allocate(pcb, block,dblock.getInstructions(),size)
            
        else:

            self.allocate(pcb, block,dblock.getInstructions(),size)
      
      
    """carga en memoria fisica las instrucciones"""  
    def allocateInMemoryPhysical(self,instructions,block):

        dirIni=block.direction
        for i in instructions:
            self.physicalMemory.setData(dirIni,i)
            dirIni+=1
            
     
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
    
   
        
class Block():
    def __init__(self,size,direction):
        self.size= size
        """esta direccion hace referencia a una direccion de memoria fisica"""
        self.direction = direction
    
    """dado otro block retorna uno nuevo compactado"""
    def compact(self,otherBlock):

        return Block(self.size+otherBlock.size,self.direction)
   

    def entersBlock(self,size):

        return  size <= self.size
    
    def entersJustBlock(self,size):

        return  size == self.size
    
    def isHigher(self,otherBlock):

        return self.size >= otherBlock.size
    
    def breakBlock(self,size):
        self.size-=size
        block=Block(size,self.size+self.direction)
        return block
  
  
"""ALGORITMOS DE BUSQUEDA DE BLOCKES"""  
        
class Setting():
    
    def getFreeBlockTo(self,size,freeBloc):

        pass # busca el bloque que me soporta uede retornar null si no lo encuentra

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
        


class Paging():
    
    def __init__(self, disk, physicalMemory,replacementAlgorithms):
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
       
    """dado un pcb carga en memoria las instrucciones""" 
    def allocateInMemoryPhysical(self,pcb,frame): 
        iss=self.disk.getInstructions(pcb)
        dir=frame.directionPhysical
        for i in iss:
            self.physicalMemory.setData(dir,i)
            dir+=1
            
    """Actualiza la tabla de pagina de pcb"""
    def updateTablePageOf(self,pcb,page,frame):
        self.pagesOfPcb[pcb].updateTablePage(page,frame)

    
    def allocateInstructionInMemoryPhysical(self,instruction,frame):
        direction=frame.directionPhysical
        for ins in instruction:
            self.physicalMemory.setData(direction,ins)
            direction+=1
    
    """obtiene y retorna todas las instrucciones del frame"""
    def getDataOfPhysical(self,frame):
        ins=[]
        direction=frame.directionPhysical
        for dir in range(self.sizePage):
            ins.append(self.physicalMemory.getData(direction))
            direction+=1
        return ins
    
    def kill(self,pcb):
        """libera los frames usados por el pcb,tambien las pages que mantiene el algoritmo de lemplazo
           
        """
        usedFrame=self.pagesOfPcb[pcb].getUsedFrames()
        self.replacementAlgorithms.removePages(self.pagesOfPcb[pcb].pages)
        del self.pagesOfPcb[pcb]
        for frame in usedFrame:
            self.takenFrame.remove(frame)
            
      
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
        pcb.addPc()
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
        nframe=pageData.getFrameOf(page)
        frame=self.paging.frames[nframe]
        kernel.swapOut(page,pcb,frame)
        return frame

    def removePages(self,pages):
        for page in pages:
            if(page in self.pages):
                self.pages.remove(page)
        
        
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

    def removePages(self,pages):
        newQueue=q.Queue()
        while(not self.queue.empty()):
            page=self.queue.get()[0]
            if(page not in pages):
                newQueue.put(page)
        self.queue=newQueue
            
            
                
                