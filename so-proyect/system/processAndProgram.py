'''
Created on 13/05/2013

@author: rodrigo
'''

"""********PROGRAMA***********"""
class Program:

    def __init__(self,path,insts):
        self.instructions=insts
        self.path=path

    def run(self):
        for x in self.instructions:
            x.execute(self.memory)

    def size(self):
        return len(self.instructions)

    def add(self,inst):
        self.instructions.append(inst)

    def getInstructions(self):
        return self.instructions


"""********PCB****************"""

class PCB():
    def __init__(self,pathProgram,pid,size):
        self.pathProgram=pathProgram
        self.pc= 0
        self.estado=State.new
        self.pid=pid
        self.size=size
        self.priority=0
        
    def addPc(self):
        self.pc+=1
    
    def getSize(self):
        return self.size
    
"""******ESTADOS DE PROCESO*******"""

class State():
    new="New"
    running="Running"
    wait="Wait"
    finished="Finished"
    ready="Ready"
    
