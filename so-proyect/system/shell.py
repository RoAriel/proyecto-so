'''
Created on 08/04/2013

@author: Di Meglio
'''

import exceptions  

class Shell:
    def __init__(self,admin,password):
        adm=User(admin,password,True)
        self.usuarios=[]
        self.usuarios.append(adm)
        self.current=adm

    def whoIAm(self):
        return self.current.userName

    def addUser(self,userName,password,isAdmin):
        if(not self.existUser(userName)):
            if(self.current.isAdmin):
                user=User(userName,password,isAdmin)
                self.usuarios.append(user)
            else:
                raise exceptions.NotPermissionsException()
        else:
            raise exceptions.UserDoesNotExistException()

    def logIn(self,userName,password):
        if(self.existUser(userName)):
            if(self.isPassword(userName, password)):
                self.current=self.getUser(userName)
            else:
                raise exceptions.IncorrectPassword()
        else:
            raise exceptions.UserDoesNotExistException()

    def isPassword(self,userName,password):
        for user in self.usuarios:
            if(user.userName==userName):
                return user.password==password

    def existUser(self,userName):
        res=False
        for user in self.usuarios:
            res= res | (user.userName==userName)
        return res

    def getUser(self,userName):
        for user in self.usuarios:
            if( user.userName==userName):
                return user


    def setAdmin(self,userName):
        if(self.current.isAdmin):
            if(self.existUser(userName)):
                self.getUser(userName).isAdmin=True
        else:
            raise exceptions.NotPermissionsException()

    def removeUser(self,userName):
        if(self.current.isAdmin):
            if(self.existUser(userName)):
                self.usuarios.remove(self.getUser(userName))
        else:
            raise exceptions.NotPermissionsException()


    def changePassword(self,newPassword,oldPassword):
        if(oldPassword==self.current.password):
            self.current.password=newPassword
        else:
            raise exceptions.IncorrectPassword()




class User:
    def __init__(self,user,password,isAdmin):
        self.userName=user
        self.password=password
        self.isAdmin=isAdmin


