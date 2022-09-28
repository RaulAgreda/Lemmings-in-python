from GameObject import GameObject
from Vector2 import Vector2
import pyxel


class LemmingDigger(GameObject):
    
    def __init__(self,tablero,startPosition,startDirection):
        super().__init__()
        self.position = startPosition
        self.direction = startDirection
        
        self.__tablero = tablero

        self.__sand_blocks = (13,14,15,0)
        self.__digDirection = Vector2(0,0)
        self.__digState = 0
        self.__setDigDirection()
        self.__tablero.setBlock(self.position + self.__digDirection,2,True)

        self.finish = False

    def __setDigDirection(self):
        """Pone la id / animación correspondiente según donde se encuentre el bloque que tiene que cavar"""

        current_block = self.__tablero.getBlock(self.position,True)

        if current_block == 12:
            if self.direction == 1:
                self.id = 8
            else:
                self.id = 9
        else:
            self.id = 10
            self.__digDirection = Vector2(0,1)


    def update(self,game_speed):
        if pyxel.frame_count%(16 if game_speed == 1 else 8) == 0:
            self.__digBlock()

    def draw_lemming(self,game_speed):
        self.draw(pyxel.frame_count//(16 if game_speed == 1 else 8))

    def __digBlock(self):
        block_coord = self.__tablero.getCoord(self.position)
        self.__tablero.setBlock(block_coord + self.__digDirection,self.__sand_blocks[self.__digState])       
        
        if self.__sand_blocks[self.__digState] == 0:
            self.finish = True
        else:
            self.__digState += 1
        