'''
Created on 08/04/2013

@author: Di Meglio
'''


class Program:

      def __init__(self,insts,mem):
          self.instructions=insts
          self.memoria=mem;

      def run(self):
          for x in self.instructions:
               x.execute(self.memoria)


      def add(self,inst):
          self.instructions.append(inst)




class Suma:


     def __init__(self,op1,op2,dest):
         self.op1=op1
         self.op2=op2
         self.dest=dest


     def execute(self,memoria):
        memoria[self.dest]=memoria[self.op1]+memoria[self.op2]



class Resta():
     def __init__(self,op1,op2,dest):
         self.op1=op1
         self.op2=op2
         self.dest=dest


     def execute(self,memoria):
        memoria[self.dest]=memoria[self.op1]-memoria[self.op2]


                            

#class ConstextoDeEjecucion:





memoria=[1212,2334,3423,1232,1232,1456,7867,8909]


instA=Suma(1,2,3)
instB=Resta(3,4,2)
instC=Resta(5,6,1)

lista =[]
program=Program(lista,memoria)
program.add(instA)
program.add(instB)
program.add(instC)

guardarMetodo=program.run
guardarMetodo()
print memoria





