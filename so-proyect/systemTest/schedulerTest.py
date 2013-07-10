'''
Created on 07/07/2013

@author: j di meglio
'''
import unittest
from mockito import *
from system.scheduler import *
from system.processAndProgram import PCB
from system.hardware import *
from system.clock import *


class TestFIFO(unittest.TestCase):


    def setUp(self):
        self.pcbA=mock(PCB)
        self.pcbB=mock(PCB)
        self.pcbC=mock(PCB)
        self.cpu=mock()
        self.policy=FCFS()

    def testAddPcb(self):
        self.policy.add(self.pcbA,self.cpu)
        self.policy.add(self.pcbC,self.cpu)
        self.policy.add(self.pcbB,self.cpu)
        
        self.assertEqual(self.policy.get(),self.pcbA,'El primer pcb no es pcbA')
        
        self.assertEqual(self.policy.get(),self.pcbC,'El segundo pcb no es pcbC')
        
        self.assertEqual(self.policy.get(),self.pcbB,'El tercer pcb no es pcbB')
        
        self.assertTrue(self.policy.isEmpty(),'Fifo todavia no esta vacio')
        
    def testGetTimer(self):
        self.assertEqual(self.policy.getTimer().__class__,Timer,"""La instancia retornada no es de Timer""")
        


class TestRoundRobin(TestFIFO):
    
    def setUp(self):
        TestFIFO.setUp(self)
        self.policy=RoundRobin(False,2)
        
    def testGetTimer(self):
        self.assertEqual(self.policy.getTimer().__class__,TimerQuantum,"""La instancia retornada no es de TimerQuantum""")

    def testAddPcbWithPriority(self):
        self.policy=RoundRobin(True,2)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()