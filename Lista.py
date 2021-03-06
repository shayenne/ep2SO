# Codigo baseado no codigo que esta disponivel em 
# http://ls.pwd.io/2014/08/singly-and-doubly-linked-lists-in-python/
# Distribuido sem quaisquer restricoes de copia

class Node(object):
 
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next
        
 
class List(object):
 
    head = None
    tail = None
    current = None
    

    def __iter__(self):
        self.current = self.head
        return self

    def next(self):
        if self.current == None:
            raise StopIteration
        else:
            self.current = self.current.next
            return self.current.prev

    def insert(self, data, prev):
        new_node = Node(data, None, None)
        if prev is not None:
            new_node.next = prev.next
            prev.next = new_node
            new_node.prev = prev
        else:
            self.append(data)
 
    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node
 
    def remove(self, node_value):
        current_node = self.head
 
        while current_node is not None:
            if current_node.data == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    if current_node.next is not None:
                        current_node.next.prev = current_node.prev
                    else:
                        self.tail = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    if current_node.next is not None:
                        current_node.next.prev = None
                    else:
                        self.tail = self.head = None
 
            current_node = current_node.next

            
    def show(self, nome):
        print "Lista Ligada da Memoria {} :".format(nome)
        current_node = self.head
        while current_node is not None:
            #print current_node.prev.data if hasattr(current_node.prev, "data") else None,
            print current_node.data, " ",
            #print current_node.next.data if hasattr(current_node.next, "data") else None
 
            current_node = current_node.next
        print "\n","-"*50
 
if __name__ == '__main__': 
    d = List()
    
    d.append(5)
    d.append(6)
    d.append(50)
    d.append(30)
    
    d.show()
    
    d.remove(50)
    d.remove(5)
    
    d.show()
