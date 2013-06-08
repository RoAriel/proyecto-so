'''
Created on 08/04/2013

@author: Di Meglio
'''

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
        MMU.__init__(disk, physicalMemory)
        self.freeBlocks= None
        self.setting = setting
        self.takenBlock= {}
        
    def allocate(self, pcb, block):
        pass # asignar un bloque al pcb si hay bloque si no lo hay compacto 
    
    def compact(self):
        pass
    
    def allocateMemory(self,pcb):
        pass
        
        
        
class Setting():
    
    def getFreeBlock(self,pcb,freeBloc):
        pass # busca el bloque que me soporta uede retornar null si no lo encuentra
    
    
        

class PhysicalMemory():
    def __init__(self,size=256):
        self.rows=range(size);
        self.size=size
            
    def getData(self,position):
        return self.rows[position]
    
    def setData(self,position,data):
        self.rows[position]=data
        
    def getSize(self):
        return self.size

        
        
class Block():
    def __init__(self,size,direction):
        self.size= size
        self.direction = direction
    
    
        
        
                

    

        
                



