import pyxel
from GameObject import GameObject
from Vector2 import Vector2
from NormalLemming import NormalLemming
from LemmingBuilder import LemmingBuilder
from LemmingBlocker import LemmingBlocker
from LemmingDigger import LemmingDigger
from SoundSystem import SoundSystem

class Lemming(GameObject):
    
    """Esta es la clase principal de Lemming"""

    def __init__(self,tablero):
        
        # job guarda el objeto del trabajo actual del lemming, la normal de caminar, la de construir, la de bloquear, y la de cavar
        self.__job = NormalLemming(tablero)

        super().__init__()

        self.__sound = SoundSystem()
        #REFERENCIA del tablero
        self.__tablero = tablero
        
        """currentJob:
        0 NormalLemming
        1 LemmingBuilder
        2 LemmingBlocker
        3 LemmingDigger"""
        self.__currentJob = 0
        
        # True cuando llega a la puerta
        self.__saved = False
  
    @property
    def position(self):
        return self.__job.position
    @position.setter
    def position(self,newPos):
        self.__position = newPos
        self.__job.position = newPos

    @property
    def direction(self):
        return self.__job.direction
    @direction.setter
    def direction(self,direction):
        self.__direction = direction
        self.__job.direction = direction

    @property
    def saved(self):
        return self.__saved

    @property
    def currentJob(self) -> int:
        """0 NormalLemming
        1 LemmingBuilder
        2 LemmingBlocker
        3 LemmingDigger"""
        return self.__currentJob

    @property
    def job(self) -> NormalLemming or LemmingBuilder or LemmingBlocker or LemmingDigger:
        return self.__job

    def update(self,game_speed):
        
        # Si es de tipo Normal, miramos si este ha cogido un item
        if self.__currentJob == 0:
            item = self.__job.getItem()
            # Si ha llegado al item escalera, se cambia a LemmingBuilder
            if item == 1:                
                self.__changeJob(1)
                self.__sound.play(self.__sound.build_sound)
            # Si ha llegado al item bloqueo, se cambia a LemmingBlocker
            elif item == 2:
                self.__changeJob(2)
                self.__sound.play(self.__sound.block_sound)
            # Si ha llegado a la pueta se salva
            elif item == 3:
                self.__saved = True
                self.__sound.play(self.__sound.enter_door_sound)
            # Si ha llegado al item de cavar
            elif item == 4:
                self.__changeJob(3)
                self.__sound.play(self.__sound.dig_sound)              
        else:
            if self.__job.finish:
                self.__changeJob(0)
        
        # Se ejecuta el update del Lemming        
        self.__job.update(game_speed)
    
    def draw_lemming(self,game_speed):
        self.__job.draw_lemming(game_speed)

    def __changeJob(self,newJob:int):
        """Cambia el trabajo al Lemming, inicializando primero los parámetros/atributos que sean necesarios\n
        @ param newJob:
        0 NormalLemming
        1 LemmingBuilder
        2 LemmingBlocker
        3 LemmingDigger"""

        self.__currentJob = newJob
        if newJob == 0:      
            newJobObj = NormalLemming(self.__tablero)      
            newJobObj.position = self.position
        elif newJob == 1:
            newJobObj = LemmingBuilder(self.__tablero)

            tableroCoord = self.__tablero.getCoord(self.position)
            # El bloque 7 es un bloque vacío como el 0 solo que este no permite colocar herramientas.
            self.__tablero.setBlock(tableroCoord, 7)

            # Pone al Lemming en el extremo del bloque según la dirección a la que mire
            posX = self.__tablero.getScreenCoord(tableroCoord).x + (0 if self.direction == 1 else self.__tablero.SIZE - 1)

            newJobObj.position = Vector2(posX - self.direction,self.position.y)

        elif newJob == 2:           
            # Se pone la posición del Lemming en el centro del bloque
            pos = self.position
            pos.x = pos.x - self.__tablero.getRelativeCoord(pos).x + 8
            newJobObj = LemmingBlocker(self.__tablero,pos)

        elif newJob == 3:
            newJobObj = LemmingDigger(self.__tablero,self.position,self.direction)

        newJobObj.direction = self.direction

        self.__job = newJobObj

    def isAlive(self) -> bool:
        """¿Está vivo?"""
        return type(self.__job) != NormalLemming or self.__job.alive