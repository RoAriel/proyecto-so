'''
Created on 08/04/2013

@author: Di Meglio
'''
import hardware

class Program:

    def __init__(self,insts,memory):
        self.instructions=insts
        self.memory=memory;

    def run(self):
        for x in self.instructions:
            x.execute(self.memory)


    def add(self,inst):
        self.instructions.append(inst)



class Instruction():
    
    def execute(self,memory):
        pass



class Suma(Instruction):


    def __init__(self,op1,op2,dest):
        self.op1=op1
        self.op2=op2
        self.dest=dest


    def execute(self,memory):
        res=memory.getData(self.op1) + memory.getData(self.op2)
        memory.setData(self.dest,res)



class Resta(Instruction):
    def __init__(self,op1,op2,dest):
        self.op1=op1
        self.op2=op2
        self.dest=dest


    def execute(self,memory):
        res=memory.getData(self.op1) - memory.getData(self.op2)
        memory.setData(self.dest,res)


                            





#Example

memory=hardware.Memory()


instA=Suma(1,2,3)
instB=Resta(3,4,2)
instC=Resta(5,6,1)

lista =[]
program=Program(lista,memory)
program.add(instA)
program.add(instB)
program.add(instC)

guardarMetodo=program.run
guardarMetodo()
print memory.rows

