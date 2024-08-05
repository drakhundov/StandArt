class Image:
    def __init__ (self, elements = []): 
        self.__elements__ = elements
    

    def get (self): 
        return self.__elements__


    def add (self, coords, colorID):
        self.__elements__.append(coords + [colorID])


    def delete (self, coords): 
        for element in self.__elements__: 
            if element[:4] == coords: 
                self.__elements__.remove(element)
        

    def clear (self): self.__elements__.clear()