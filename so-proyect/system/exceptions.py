'''
Created on 08/04/2013

@author: Di Meglio
'''

class UserDoesNotExistException(Exception):

    def __init__(self):
        Exception.__init__(self)


class UserAlreadyExistsException(Exception):

    def __init__(self):
        Exception.__init__(self)



class NotPermissionsException(Exception):

    def __init__(self):
        Exception.__init__(self)
        
class IncorrectPassword(Exception):
    
    def __init__(self):
        Exception.__init__(self)
