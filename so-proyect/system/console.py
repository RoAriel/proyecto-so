'''
Created on 08/04/2013

@author: Di Meglio
'''
import sys
import exceptions as e
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
        print '>*****All Comands****'
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
            if(res[3]=='s'):
                isAdmin=True
            else:
                if res[3]!='n' :
                    print ">Error",res[3] ,' s/n'
                    return
            try:
                shell.addUser(res[1],res[2],isAdmin)
            except e.UserAlreadyExistsException:
                print ">User Already Exists"
            except  e.NotPermissionsException:
                print ">Not Permissions"
                
    
class ShowUsers():
    def __init__(self):
        self.name='showUsers'
        self.description='show All Users'
        
    def execute(self,shell,inPut,console):
        print '>*****All Users****'
        for user in shell.users:
            print '> ',user.userName
          
  
  
class Exit():
    def __init__(self):
        self.name='exit'
        self.description='end of shell'
        
    def execute(self,shell,inPut,console):
        console.running=False
    
class LogIn():
    
    def __init__(self):
        self.name='logIn'
        self.description='Login user'
        
    def execute(self,shell,inPut,console):
        res=inPut.split()
        try:
            shell.logIn(res[1],res[2])
        except e.UserDoesNotExistException:
            print "User does not exist"
            
class LogOut():
    
    def __init__(self):
        self.name='logOut'
        self.description='Logout user current'
        
    def execute(self,shell,inPut,console):
        res=inPut.split()
        shell.logOut()      
       
class ChangePassword():  
    
    def __init__(self):
        self.name='changePassword'
        self.description='Change password of the user current'
        
    def execute(self,shell,inPut,console):
        res=inPut.split()
        try:
            shell.changePassword(res[1],res[2])
        except e.IncorrectPassword:
            print "password incorrect" 
    
    
class RemoveUser():  
    
    def __init__(self):
        self.name='removeUser'
        self.description='Change password of the user current'
        
    def execute(self,shell,inPut,console):
        res=inPut.split()
        try:
            shell.removeUser(res[1])
        except e.UserDoesNotExistException:
            print "user does not exist" 
        except e.NotPermissionsException:
            print "not permissions"
    
    
            
    
shell=Shell(sys.argv[1],sys.argv[2]);
lisComand=[AddUser(),Help(),Exit(),ShowUsers(),LogIn(),ChangePassword(),RemoveUser()] 
console=Console(shell,lisComand) 
console.run()        
         
            
                
        

        
    