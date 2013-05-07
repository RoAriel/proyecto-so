'''
Created on 06/05/2013

@author: usuario
'''


class Queue():
    
    def __init__(self):
        self.elements=[]
    
    
    def add(self,element):
        self.elements.append(element)
        
    def get(self):
        process=self.elements[0]
        self.elements.remove(process)
        return process
        
    def isEmpty(self):
        return len(self.elements)==0
    
    
    
class PriorityQueue():
    
    def __init__(self,comparator):
        self.elements=[]
        self.comparator=comparator
    
    def add(self,element):
        self.elements.append(element)
                
    def get(self):
        elementMax=self.elements[0]
        for p in self.elements:
            if(self.comparator(p,elementMax)<0):
                elementMax=p
        self.elements.remove(elementMax)
        return elementMax
        
    def isEmpty(self):
        return len(self.elements)==0    
