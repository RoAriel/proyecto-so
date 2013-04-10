'''
Created on 08/04/2013

@author: Jose
'''
import sys
import exceptions
from shell import Shell



class Console():
    def __init__(self,shell,comands):
        self.comands=comands
        self.shell=shell
        self.running=True
        
            
    def searchComandAndExecute(self,inPut,console):
        res=inPut.split()
        for comand in self.comands:
            if(comand.name==res[0]):
                comand.execute(self.shell,inPut,self)
               
                
    def run(self):
        while(self.running):
            input=raw_input('>')
            self.searchComandAndExecute(input,self)
            
            
class Help():
    def __init__(self):
        self.name='help'
        self.description=''
        
    def execute(self,shell,inPut,console):
        for comand in console.comands:
            print '>*',comand.name,'-->',comand.description
             
            
class AddUser():
    def __init__(self):
        self.name='addUser'
        self.description='<UserName> <Password> <isAdmin s/n>'
        
    def execute(self,shell,inPut,console):
        res=inPut.split()
        if(len(res)==4):
            isAdmin=False
            if(res[2]=='s'):
                isAdmin=True
            try:
                shell.addUser(res[1],res[2],isAdmin)
            except exceptions.UserAlreadyExistsException:
                print "El usuario ya existe"
            except  exceptions.NotPermissionsException:
                print "El usuario fue agregado correctamente"
    
class ShowUsers():
    def __init__(self):
        self.name='showUsers'
        self.description='<UserName> <Password> <isAdmin s/n>'
        
    def execute(self,shell,inPut,console):
        for user in shell.users:
            print user.userName
      
  
  
class Exit():
    def __init__(self):
        self.name='exit'
        self.description='<UserName> <Password> <isAdmin s/n>'
        
    def execute(self,shell,inPut,console):
        console.running=False
        
    
    
            
     
shell=Shell(sys.argv[1],sys.argv[2]);
lisComand=[AddUser(),Help(),Exit(),ShowUsers()] 
console=Console(shell,lisComand) 
console.run()        
         
            
                
        

        
    