""" 
Esta clase la usamos como herramienta, crear un Vector2 es mucho más rápido que crear 
dos variables para cada coordenada, además podemos utilizar operaciones directas entre dos vectores
mediante operadores como suma, resta o multiplicación por escalares
"""
class Vector2:
    """
    Vector2(xy:Vector2)\n
    Vector2(xy:tuple)\n
    Vector2(x:int,y:int)"""
    def __init__(self, x = 0,y = 0):
        
        if type(x) == tuple:
            self.x = x[0]
            self.y = x[1]
        elif type(x) == Vector2:
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y

    @property 
    def x(self):
        return self.__x

    @x.setter
    def x(self,value):
        if type(value) == int:
            self.__x = value
        else:
            raise ValueError("Value must be int not "+str(type(value)))
    
    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self,value):
        if type(value) == int:
            self.__y = value
        else:
            raise ValueError("Value must be int not "+type(value)+str(type(value)))

    def setXY(self,vector):
        self.x,self.y = vector.x, vector.y

    def asTuple(self):
        return self.x,self.y

    def magnitude(self):
        return (self.x ** 2 + self.y **2) ** 0.5

    def distance(self,b):
        return ((b.x-self.x) ** 2 + (b.y-self.y) **2) ** 0.5

    # +
    def __add__(self,b):
        if type(b) == Vector2:
            return Vector2(self.x+b.x,self.y+b.y)
        elif type(b) == tuple:
            return Vector2(self.x + b[0], self.y + b[1])

    # +=
    def __iadd__(self,b):
        if type(b) == Vector2:
            return Vector2(self.x+b.x,self.y+b.y)
        elif type(b) == tuple:
            return Vector2(self.x + b[0], self.y + b[1])

    # -
    def __sub__(self,b):
        if type(b) == Vector2:
            return Vector2(self.x-b.x,self.y-b.y)
        elif type(b) == tuple:     
            return Vector2(self.x - b[0], self.y - b[1])

    # -=
    def __isub__(self,b):
        if type(b) == Vector2:
            return Vector2(self.x-b.x,self.y-b.y)
        elif type(b) == tuple:     
            return Vector2(self.x - b[0], self.y - b[1])

    # -vector
    def __neg__(self):
        return Vector2(self.x*-1,self.y*-1)

    # ==
    def __eq__(self,b):
        if type(b) == Vector2:
            return self.x == b.x and self.y == b.y
        elif type(b) == tuple: 
            return self.x == b[0] and self.y == b[1]

    # !=
    def __ne__(self,b):
        if type(b) == Vector2:
            return self.x != b.x or self.y != b.y
        elif type(b) == tuple: 
            return self.x != b[0] or self.y != b[1]

    # *
    def __mul__(self,b):
        """Producto escalar entre dos vectores o vector por escalar"""
        if type(b) == int:
            return Vector2(self.x * b,self.y * b)
        elif type(b) == Vector2:
            return (self.x * b.x) + (self.y * b.y)
        elif type(b) == tuple:
            return (self.x * b[0]) + (self.y * b[1])

    # *= 
    def __imul__(self,b):
        return Vector2(self.x * b,self.y * b)

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"