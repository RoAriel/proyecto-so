'''
Created on 07/07/2013

@author: CABJ
'''
import unittest
from mockito import *
from scheduler import *
from processAndProgram import PCB
from hardware import *


class TestFIFO(unittest.TestCase):


    def setUp(self):
        self.pcbA=mock(PCB)
        self.pcbB=mock(PCB)
        self.pcbC=mock(PCB)
        self.cpu=mock()
        self.fifo=FCFS()

    def testAddPcb(self):
        self.fifo.add(self.pcbA,self.cpu)
        self.fifo.add(self.pcbC,self.cpu)
        self.fifo.add(self.pcbB,self.cpu)
        
        self.assertEqual(self.fifo.get(),self.pcbA,'El primer pcb no es pcbA')
        
        self.assertEqual(self.fifo.get(),self.pcbC,'El segundo pcb no es pcbC')
        
        self.assertEqual(self.fifo.get(),self.pcbB,'El tercer pcb no es pcbB')
        
        self.assertTrue(self.fifo.isEmpty(),'Fifo todavia no esta vacio')




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()