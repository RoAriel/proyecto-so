'''
Created on 19/04/2013

@author: j di meglio
'''

import scheduler
from interruptions  import Interruption 
from processAndProgram import State
from processAndProgram import PCB

"""***********MEMORIA FISICA**************"""

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

 
"""************cpu***************"""


class CPU():
    
    
    def __init__(self,memory,mode):
        self.memory=memory
        self.mode=mode
        self.pcb=None
    

    def setProcess(self,pcb):
        self.pcb=pcb
        
    def click(self):
       
        if( self.mode.isModeUser() and (self.pcb is not None)): 
            self.pcb.state=State.running
            instruction=self.memory.fetchInstruction(self.pcb) 
            if instruction is not None:
                instruction.execute(self.pcb)
                
    def kill(self,pcb):
        if(self.pcb == pcb):
            self.pcb=None
            
"""**********DISCO**************"""   


class Disk():
    
    def __init__(self,sizeBlock):
        self.sizeBlock=sizeBlock
        self.programs={}
        self.swap={}
        """Por bloque"""
        self.freeSwap=1024 

    """Dado un programa lo parte en bloques y lo guarda junto al path del programa"""   
    def addProgram(self,program):
        size=program.size()
        instructions=program.getInstructions()
        amountBlock=self.getAmountBlock(size)
        number=0
        blocks=[]
        end=False
        nblock=0
        for i in range(amountBlock):
            list=[]
            for n in range(self.sizeBlock):
                if(number != len(instructions)):
                    
                    list.append(instructions[number])
                    number+=1
                else:
                    self.programs[program.path]=blocks
                    end=True
                    break
            blocks.append(DiskBlock(list,nblock))
            nblock+=1
            if end:
                break
        self.programs[program.path]=blocks
                
    """si la pagina esta en disco swap retorna esa,si no bussca el programa """          
    def getBlock(self,page,pid,pathProgram):
        if(self.inSwap(pid,page,pathProgram)):
            return self.swap[pid][page.direction]
        return self.programs[pathProgram][page.direction]
    
    """Retorna true si esta el pcb en swap con su pagina page """
    def inSwap(self,page,pid,pathProgram):
        if (pid in self.swap.keys()):
            for blockSwap in self.swap[pid]:
                if(blockSwap.direction == page.direction):
                    return True
        return False
    
    def getDiskBlock(self,pcb):
        blocks=self.programs[pcb.pathProgram]
        listInstructions=[]
        for block in blocks:
            for instruction in block.getInstructions():
                listInstructions.append(instruction)
        return DiskBlock(listInstructions)
            
    
    """Retorna la cantidad de bloques que se necesitan para un programa de
       tamanho size
    """  
    def getAmountBlock(self,size):
        if(size % self.sizeBlock == 0):
            return size/self.sizeBlock
        else:
            return size/self.sizeBlock+1
    
    """guarda en disco swap las instrucciones del pcb""" 
    def save(self,pcb,page,instructions):  
        block=DiskBlock(instructions,page.direction) 
        if(pcb.pid not in self.swap.keys()):
            self.swap[pcb.pid]=[]
        self.swap[pcb.pid].append(block)
        
    
    def removePcbInSwap(self,pid):
        if(pid in self.swap.keys()):
            del(self.swap[pid])
    
    def programExists(self,pathProgram):
        return pathProgram in self.programs.keys()
    
    """Dado un path de programa retorna su tamanho"""
    def getSizeProgram(self,pathProgram):
        size=0
        for block in self.programs[pathProgram]:
            size+=len(block.getInstructions())
        return size
    
    """Retorna el tamanho  libre en disco swap,simplemente suma la cantidad de bloques en swap y se lo resta a freeSwap"""
    def getFreeSwapSpace(self):
        blockSwap=self.swap.values()
        totalBlockSwap=0
        for listBlocks in blockSwap:
            totalBlockSwap+=len(listBlocks)
        return self.freeSwap - totalBlockSwap
    
class DiskBlock():
    
    def __init__(self,instructions,direction=None):
        self.instructions=instructions
        self.direction=direction
    
    def getInstructions(self):
        return self.instructions
    
    def size(self):
        return len(self.instructions)
    

"""Generador de pids"""
class PidGenerator():
    
    inital=0
    
     
    @classmethod      
    def getPid(self):
        pid=PidGenerator.inital
        PidGenerator.inital+=1
        return pid
 