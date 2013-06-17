'''
Created on 08/04/2013

@author: Di Meglio
'''

from process import PCB

import instructions as i
import process as p
import random






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
#         hayOcurrenciaMayo(self.freeBlocks)
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
         
    def getData(self,pcb):
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
            """si se compacta  y block sigue siendo none,quiere decir que no hay espacion,el pcb no puede ser
               guardado en memoria en este momento
            """
            block=self.compactTo(size)
            if(block is not  None):

                self.allocate(pcb, block,dblock.getInstructions(),size)
            else:
                print 'no se guardo'
        else:

            self.allocate(pcb, block,dblock.getInstructions(),size)
      
      
    """carga en memoria fisica las instrucciones"""  
    def allocateInMemoryPhysical(self,instructions,block):

        dirIni=block.direction
        for i in instructions:
            self.physicalMemory.setData(dirIni,i)
            print 'llego ',dirIni
            dirIni+=1
            
     
    """Libera la memoria usada por el pcb"""   
    def free(self,pcb):
        i=self.takenBlock.keys()
        res=False
        for n in i:
            if(n == pcb):
                res=True
        if(not res):
            return
        """"""
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
    





class Disk():
    
    def getDiskBlock(self,pcb):

        return DBlock()
    
class DBlock():
    
    def __init__(self):

        self.list=self.generate()
        
            
    def generate(self):
        list=[]
        for p in range(random.randrange(1,19)):
            list.append(i.Cpu())
        list.append(i.Finalize())
        return list
    
    def getInstructions(self):

        return self.list
    
    def size(self):

        return len(self.list)
        
        
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

def getBlockId(dir,list):

    res=[]
    for x in list:
        if(x.direction == dir):
            res.append(x)
    return res

def sonIguales(list):

    res=True
    p=list[0]
    for x in list:
        res&=p == x
    return res

def hayOcurrenciaMayo(lista):

    for x in lista:
        if(ocurrenciasDe(x.direction,lista)>1):
            print 'hay mayor a 1'
        else:
            print 'no hay'

def ocurrenciasDe(dir,lista):

    ocu=0
    for b in lista:
        if(dir == b.direction):
            ocu+=1
    return ocu
    
ac=ContinuousAssignment(Disk(),PhysicalMemory(30),WorstFit())

p0=PCB(0,0,0,0,0)

"""
ac.allocateMemory(p0)
print ac.takenBlock[p0].direction
print ac.getData(p0)
ac.free(p0)

for i in range(11265):
    p0=PCB(0,0,0,0,0)
    ac.allocateMemory(p0)
    ac.free(p0)
"""

"""pruebaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas"""
"""
print '-----------------'
print 'blockes libres: ',len(ac.freeBlocks)
tam=0
for b in ac.freeBlocks:
   print 'size: ',b.size
   print 'direccion:',b.direction 
   tam+=b.size
print 'size total:',tam
"""
"""

print len(ac.freeBlocks)
print ac.freeBlocks[0].size
print ac.freeBlocks[0].direction
print len(ac.takenBlock.values())
"""

"""
print 'ocurrencias:'
for i in range(10):
    ocu=ocurrenciasDe(i, ac.freeBlocks)
    print 'ocurrencias de: ', i, 'son: ',ocu
    res=getBlockId(i,ac.freeBlocks)
    if(len(res)>1):
        print 'iguales? :',sonIguales(res)

hayOcurrenciaMayo(ac.freeBlocks)

nn=[1,2,3]
nn.insert(0, 4)
"""