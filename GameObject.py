import pyxel
from Vector2 import Vector2

# Clase padre de todas las clases de Lemming
class GameObject:  

    def __init__(self):
        self.position = Vector2(0,0)
        self.direction = 1
        self.id = 0

    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self,position:Vector2):
        if type(position) == Vector2:
            self.__position = position
        else:
            raise ValueError("Position must be a Vector2")
    
    @property
    def direction(self):
        return self.__direction
    @direction.setter
    def direction(self,direction):
        if direction in (-1,0,1):
            self.__direction = direction
        else:
            raise ValueError("direction must be -1 or 0 or 1")

    # Dibuja el Lemming
    def draw(self,animF = 0):
        """Dibuja según el id del lemming, y animF indica el fotograma de la animación"""
        #frameSize es el tamaño de la imagen de izquierda a derecha en píxeles / tamaño de cada fotograma de la animación
        frameSize = 6
        #nFrames es el número de fotogramas que tiene cada animación
        nFrames = 4
        #Aquí modificamos el nº de fotogramas y su tamaño según la id de la animación
        if self.id in (0,1,2,3):
            frameSize = 6
            nFrames = 4
        elif self.id in (4,5):
            frameSize = 10
            nFrames = 6
        elif self.id in (6,7):
            frameSize = 8
            nFrames = 7
        elif self.id in (8,9,10):
            frameSize = 16
            nFrames = 2

        #offset es para que se ajusten las coordenadas con respecto al centro del dibujo (Solo eje x)
        offset = frameSize // 2
        #Dibujamos
        pyxel.blt(self.position.x - offset, self.position.y-15, 0, animF % nFrames * frameSize, self.id*16, frameSize, 16,0)