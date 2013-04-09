'''
Created on 08/04/2013

@author: Jose
'''
from shell import Shell
import exceptions

        
class Conole():
    def __init__(self,comands):
        self.comands=comands
        
    def help(self):
        for comand in self.comands:
            print comand.name,comand.desription
            
    def searchComand(self,shell,inPut):
        res=inPut.split()
        for comand in self.comands:
            if(comand.name==res[0]):
                     
            
class addUser():
    def __init__(self,comands):
        self.name='addUser'
        self.description='<UserName> <Password> <isAdmin s/n>'
        
    def execute(self,shell,inPut):
        res=inPut.split()
        if(res.size()==3):
            isAdmin=False
            if(res[2]=='s'):
                isAdmin=True
            try:
                shell.addUser(res[0],res[1],isAdmin)
            except exceptions.UserAlreadyExistsException:
                print "El usuario ya existe"
            except  exceptions.NotPermissionsException:
                print "El usuario fue agregado correctamente"
            
            
                
            
                
        

        
    