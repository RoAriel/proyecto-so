'''
Created on 08/04/2013

@author: Di Meglio
'''
import unittest
import exceptions
from shell import Shell

class Test(unittest.TestCase):


    def setUp(self):
        self.shell=Shell("Jose","1234")
    


    def testAddUserWithAdmin(self):
        self.shell.addUser("userName", "password", True)
        user=self.shell.users[1]
        self.assertEquals(user.userName ,"userName","El nombre pasadopor parametro no coincide con el guardado en la shell");
        self.assertEquals(user.password ,"password","El password pasadopor parametro no coincide con el guardado en la shell");
        self.assertEquals(user.isAdmin ,True,"El usuario no tiene los permisos correctos");

    def testAddUserNotAdmin(self):
        self.shell.addUser("userName", "password", False)
        self.shell.logIn("userName", "password")
        
        try:
            self.shell.addUser("Jose", "password", False)
            self.fail("se esperaba NotPermissionsException")
        except exceptions.NotPermissionsException:
            pass
        
    def testAddUserAlredyExists(self):
        self.shell.addUser("userName", "password",False)
        
        try:
            self.shell.addUser("userName", "other",False)
        except exceptions.UserAlreadyExistsException:
            pass
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()