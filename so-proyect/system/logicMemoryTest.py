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

class Test(unittest.TestCase):


    def setUp(self):
        self.disk=mock(Disk)
        self.physicalMemory=mock(PhysicalMemory)
        self.plp=mock(PLP)
        self.pcbA=mock(PCB)
        self.pcbB=mock(PCB)
        self.pcbC=mock(PCB)
        self.dickBlockA=mock(DiskBlock)
        self.dickBlockB=mock(DiskBlock)
        self.dickBlockC=mock(DiskBlock)
        
        """Config mocks"""
        when(self.physicalMemory).getSize().thenReturn(24)
    
        
        self.memory=ContinuousAssignment(self.disk,self.physicalMemory,None,self.plp)


    def testMemoryCreated(self):
        self.assertEqual(len(self.memory.freeBlocks),1,'Se creo mas de un bloque o menos')
        self.assertEqual(self.memory.freeBlocks[0].size,24,'El tamanho no es 24')
        self.assertEqual(self.memory.freeBlocks[0].directionPhysical,0,'El bloque no cominza con la direccion fisica 0')
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()