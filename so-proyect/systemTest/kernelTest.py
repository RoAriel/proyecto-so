'''
Created on 07/07/2013

@author: j di meglio
'''
import unittest
from mockito import *
from system.logicMemory import *
from system.hardware import *
from system.plp import *
from system.processAndProgram import *
from system.instructions import *
from system.kernel import *
from system.scheduler import *

class TestKernel(unittest.TestCase):


    def setUp(self):
        self.disk=mock(Disk)
        self.physicalMemory=mock(PhysicalMemory)
        self.memory=mock(Paging)
        self.mode=mock(Mode)
        self.cpu=mock(CPU)
        self.policy=mock(FCFS)
        self.plp=mock(PLP)
        
        
        self.kernel=Kernel(self.cpu,self.physicalMemory,self.memory,self.policy,self.disk,self.mode)
        self.kernel.plp=self.plp
        
    def testExecuteProgram(self):
        when(self.disk).programExists('myProgram').thenReturn(True)
        self.kernel.executeProgram('myProgram')
        
        verify(self.disk).programExists('myProgram')
        verify(self.plp).allocateMemory(any(PCB))
        verify(self.mode).setModeUser()
        verify(self.mode).setModeKernel()
        
    def testAddPcb(self):
        pcb=mock(PCB)
        self.kernel.addPcb(pcb)
        
        verify(self.plp).allocateMemory(pcb)
        verify(self.mode).setModeUser()
        verify(self.mode).setModeKernel()
        
    def testKill(self):
        pcb=mock(PCB)
        self.kernel.kill(pcb)
        verify(self.memory).kill(pcb)
        
    def testSwapOut(self):
        pcb=mock(PCB)
        page=mock(Page)
        frame=mock(Frame)
        self.kernel.swapOut(page, pcb, frame)
        
        verify(self.memory).getDataOfPhysical(frame)


        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()