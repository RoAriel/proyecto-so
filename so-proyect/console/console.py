'''
Created on 09/07/2013

@author: CABJ
'''



class Console():
    
    def __init__(self):
        self.commands=None
        self.kernel=None
        self.running=True
        
    def start(self):
        self.kernel.start()
    
    def run(self):
        while(self.running):
            input=raw_input('>')
            self.execute(input)
            
    def execute(self,input):
        behavior=self.commands[input[0]]
        if(behavior is not None): 
            behavior(input)
        else:
            pass
        
    def validateNamberParam(self,n1,n2):
        if(n1 != n2):
            pass
        
        
    def startKernel(self,input):
        self.validateNamberParam(len(input)-1, 0)
        self.kernel.start()
        
    def stopKernel(self,input):
        self.validateNamberParam(len(input)-1, 0)
        self.kernel.stop()
        
    def executeProgram(self):
        self.validateNamberParam(len(input)-1, 1)
        
    def ps(self,input):
        self.validateNamberParam(len(input)-1, 0)
        self.showReedyProcess()



class Command():
    
    start='start'
    stop='stop'
    execute='execute'