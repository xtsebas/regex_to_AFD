class Stack:
    def __init__(self):
        self.items = []
        
    
    def push(self, item):
        """
        Inserta un item en el stack
        """
        self.items.append(item)
    
    def pop(self):
        """
        Elimina y devuelve el ultimo elemento en la pila
        Si la pila esta vacio devuelve None
        """
        if len(self.items) == 0:
            return None
        else:
            return self.items.pop(0)
    
    def peek(self):
        """
        Devuelve el ultimo elemento en la pila sin eliminarlo
        Si la pila esta vacio devuelve None
        """
        if len(self.items) == 0:
            return None
        else:
            return self.items[0]
        
    def is_empty(self):
        return len(self.items) == 0