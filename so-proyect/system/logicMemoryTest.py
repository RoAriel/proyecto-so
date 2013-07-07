'''
Created on 07/07/2013

@author: CABJ
'''
import unittest
from mockito import *
from logicMemory import *
from hardware import *
from plp import *
from processAndProgram import *
from instructions import *

class TestContinuousAssignment(unittest.TestCase):


    def setUp(self):
        self.disk=mock(Disk)
        self.physicalMemory=mock(PhysicalMemory)
        self.plp=mock(PLP)
        self.pcbA=mock(PCB)
        self.pcbB=mock(PCB)
        self.pcbC=mock(PCB)
        self.disckBlockA=mock(DiskBlock)
        self.disckBlockB=mock(DiskBlock)
        self.disckBlockC=mock(DiskBlock)
        self.instructionsA=[mock(CPU),mock(CPU),mock(CPU),mock(CPU),mock(Finalize)]
        self.instructionsB=[mock(CPU),mock(Finalize)]
        self.instructionsC=[mock(CPU),mock(CPU),mock(CPU),mock(Finalize)]
        self.setting=mock(FirstFit)
        
        """Config mocks"""
        when(self.physicalMemory).getSize().thenReturn(6)
        
        when(self.pcbA).getSize().thenReturn(5)
        
        when(self.pcbB).getSize().thenReturn(2)
        
        when(self.pcbC).getSize().thenReturn(4)
        
        when(self.disk).getDiskBlock(self.pcbA).thenReturn(self.disckBlockA)
        
        when(self.disk).getDiskBlock(self.pcbB).thenReturn(self.disckBlockB)
        
        when(self.disk).getDiskBlock(self.pcbC).thenReturn(self.disckBlockC)
        
        when(self.disckBlockA).getInstructions().thenReturn(self.instructionsA)
        
        when(self.disckBlockB).getInstructions().thenReturn(self.instructionsB)
        
        when(self.disckBlockC).getInstructions().thenReturn(self.instructionsC)
        
    
        
        self.memory=ContinuousAssignment(self.disk,self.physicalMemory,self.setting,self.plp)


    def testMemoryCreated(self):
        self.assertEqual(len(self.memory.freeBlocks),1,'Se creo mas de un bloque o menos')
        self.assertEqual(self.memory.freeBlocks[0].size,6,'El tamanho no es 24')
        self.assertEqual(self.memory.freeBlocks[0].directionPhysical,0,'El bloque no cominza con la direccion fisica 0')
    
    def testAllocateMemoryWithFirstFit(self):  
        when(self.setting).getFreeBlockTo(5,self.memory.freeBlocks).thenReturn(self.memory.freeBlocks[0])
        self.memory.allocateMemory(self.pcbA)
        self.assertEqual(self.memory.freeBlocks[0].size,1,'El tamanho no es 1')
        self.assertEqual(self.memory.freeBlocks[0].directionPhysical,0,'La direccion fisica del bloque no es 0')
    
    def testKillPcb(self): 
        when(self.setting).getFreeBlockTo(5,self.memory.freeBlocks).thenReturn(self.memory.freeBlocks[0])
        self.memory.allocateMemory(self.pcbA)
        self.memory.kill(self.pcbA)
        self.assertEqual(self.memory.freeBlocks[0].size,1,'El tamanho no es 1')
        self.assertEqual(self.memory.freeBlocks[1].size,5,'El tamanho no es 5')
        self.assertEqual(len(self.memory.freeBlocks),2,'Los bloques libres no son 2')
        
    def testCompact(self):
        """Guarda un proceso de size 2 ,luego lo mata"""
        when(self.setting).getFreeBlockTo(2,self.memory.freeBlocks).thenReturn(self.memory.freeBlocks[0])
        self.memory.allocateMemory(self.pcbB)
        self.memory.kill(self.pcbB)
        
        """Guarda otro proceso de size 2,debe compactar porque hay dos bloques uno de size 2 y otro de 4"""
        when(self.setting).getFreeBlockTo(5,self.memory.freeBlocks).thenReturn(None)
        self.memory.allocateMemory(self.pcbA)
        
        """Solo hay un bloque de size 1"""
        self.assertEqual(self.memory.freeBlocks[0].size,1,'El tamanho de bloque no es 1')
        self.assertEqual(self.memory.freeBlocks[0].directionPhysical,0,'la direccion fisica no es 0')
        self.assertEqual(len(self.memory.freeBlocks),1,'El tamanho no es 1')
        
        """Se elimina el pcbB de memoria"""
        self.memory.kill(self.pcbA)
        
        """Deben quedar dos bloques libres"""
        self.assertEqual(len(self.memory.freeBlocks),2,'El tamanho no es 2')
        """El primero de size 1"""
        self.assertEqual(self.memory.freeBlocks[0].size,1,'El tamanho de bloque no es 1')
        self.assertEqual(self.memory.freeBlocks[0].directionPhysical,0,'la direccion fisica no es 0')
        
        """y el segundo de size 5"""
        self.assertEqual(self.memory.freeBlocks[1].size,5,'El tamanho de bloque no es 5')
        self.assertEqual(self.memory.freeBlocks[1].directionPhysical,1,'la direccion fisica no es 1')
        

        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()