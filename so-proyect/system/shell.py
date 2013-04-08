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
                print "El usuario se agrego correctamente"
            else:
                print "No tines permisos para agregar nuevo usuario"
        else:
            print "El usuario ya existe hdp"

    def logIn(self,userName,password):
        if(self.existUser(userName)):
            if(self.isPassword(userName, password)):
                self.current=self.getUser(userName)
                print "Te has logeado correctamente"
            else:
                print "Password incorrecta"
        else:
            print "El usuario no existe"

    def isPassword(self,userName,password):
        for user in self.usuarios:
            if(user.userName==userName):
                return user.password==password

    def existUser(self,userName):
        res=False
        for user in self.usuarios:
            res= res | (user.userName==userName)
            if(res):
             #   raise UserDoesNotExistException()
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
           # raise NotPermissionsException()

    def removeUser(self,userName):
        if(self.current.isAdmin):
            if(self.existUser(userName)):
                self.usuarios.remove(self.getUser(userName))
                print "El usuario fue eliminado correctamente"
        else:
           # raise NotPemisionsException()


    def changePassword(self,newPassword,oldPassword):
        if(oldPassword==self.current.password):
            self.current.password=newPassword
            print "Cambio de contrasenia correctamente"
        else:
            print "Constrasenia incorrecta"




class User:
    def __init__(self,user,password,isAdmin):
      self.userName=user
      self.password=password
      self.isAdmin=isAdmin




raise UserDoesNotExistException(Exception)
