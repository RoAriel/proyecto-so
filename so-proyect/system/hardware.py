'''
Created on 08/04/2013

@author: Di Meglio
'''

import process as p

class MMU():
    
    def __init__(self, disk, physicalMemory):
        self.disk = disk
        self.physicalMemory = physicalMemory
        
    def allocateMemory(self,pcb):
        pass
    
    def free(self, pcb):
        pass
    
    def getInstruction(self,pcb):
        pass
    
    
class ContinuousAssignment(MMU):
    
    def __init__(self, disk, physicalMemory,setting):
        MMU.__init__(self,disk, physicalMemory)
        self.freeBlocks=self.generateFreeBlock(physicalMemory)
        self.setting = setting
        self.takenBlock={}#es un diccionario,la clave es el pcb y el valor un bloque asignado
     
    """chequea que block no sea none,si no es None le asigna al pcb el block(en takenBlock) una vez asignado
       elimina el block de freeBlock y carga en memoria fisica las instrucciones.
       En el caso en el que block se None,se debe compactar la memoria,si compactTo retorna un bloke se debe repetir
       la primera parte,si retorna none quiere decir que no hay espacio en memoria debe esperar(la parte de espera nose ,hay
       que preguntar)
    """    
    def allocate(self, pcb, block,instructions):
        pass 
    
    
    
    """dado una size compacta la memoria logica y retorna el bloque detamanho size ,en el caso que retorne none
       quiere decir que no hay suficiente espacio
    """
    def compactTo(self,size):
        sizeAll=0
        for block in self.freeBlocks:
            sizeAll+=block.size
            
        newBlock=Block(sizeAll,0)
        self.moveBlocks(sizeAll)
        
        self.freeBlocks=[newBlock]
        if newBlock.entersBlock(size):
            return newBlock.breakBlock(size)
        return None
    
    def moveBlocks(self,directinoIni):
        dir=directinoIni
        taken=self.takenBlock.values()
        for block in taken:
            instructions=self.getInstructions(block)
            block.direction=dir
            self.allocateInstructions(instructions,block)
            dir+=block.size
    
    """dado el tamanho de memoria fisica generia un block free""" 
    def generateFreeBlock(self,physicalMemory):
        return [Block(physicalMemory.getSize(),0)]
    
     
    def allocateMemory(self,pcb):
        """obtiene las instrucciones del pcb almacenadas en disco y calcula el tamanho"""
        dblock=self.disk.getData(pcb)
        size=dblock.size()
        """ delega al ajuste la buqueda de un bloque de tamanho size,puede no encotrarlo,en ese caso
            retorna none
        """
        block=self.setting.getFreeBlockTo(size,self.freeBlocks)
        """le asigna al pcb el block y lo carga en memoria fisica"""
        if(block is not None):
            block=self.compactTo(size)
            if(block is not None):
                self.allocate(pcb, block,dblock)
            else:
                pass
        else:
            self.allocate(pcb, block,dblock)
      
      
    """este metodo debe cargar en memoria fisica las instrucciones,tener en cuenta el block(tiene direction y size)"""  
    def allocateInMemoryPhisical(self,instructions,block):
        pass
     
    """este es muy facil,libera el bloquedel pcb de memorua logica(la fisica no la toca)"""   
    def free(self,pcb):
        pass
  
        
class Block():
    def __init__(self,size,direction):
        self.size= size
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
        
        
class Setting():
    
    def getFreeBlockTo(self,size,freeBloc):
        pass # busca el bloque que me soporta uede retornar null si no lo encuentra

class FirstFit(Setting):
    
    def getFreeBlockTo(self, size, freeBloc):
        for block in freeBloc:
            if(block.entersBlock(block)):
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
        blockMax=freeBlock[0]
        for block in freeBlock:
            if(not blockMax.isHigher(block)):
                blockMax=block
        if(blockMax.entersBlock(size)):
            return blockMax
        return None
    




""" esto es para que pruebes,como el dico no lo tenemos hecho
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

""" 
        
"""MEMORIA FISICA"""
class PhysicalMemory():
    def __init__(self,size=4000):
        self.rows=range(size);
        self.size=size
            
    def getData(self,position):
        return self.rows[position]
    
    def setData(self,position,data):
        self.rows[position]=data
        
    def getSize(self):
        return self.size

        
   
"""pequenha prueba de compactTo"""
    
