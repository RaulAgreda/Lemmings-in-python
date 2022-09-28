import pyxel
from GameObject import GameObject
from Vector2 import Vector2

class LemmingBuilder(GameObject):

    def __init__(self,tablero):
        super().__init__()
        
        self.__tablero = tablero

        self.__blocks = []
        self.finish = False

    def update(self,game_speed):
        self.__setBlock(game_speed)
        
        self.id = 6 if self.direction == 1 else 7
    
    def draw_lemming(self,game_speed):
        self.draw(pyxel.frame_count//(6 // game_speed))
        self.__drawBlocks()

    def __setBlock(self,game_speed):
        """Construye la escalera bloque a bloque"""

        if len(self.__blocks) < 8:
            if pyxel.frame_count % (20 // game_speed) == 0:
                self.__blocks.append(Vector2())
                for i in range(len(self.__blocks)):
                    newBlockPosX = 0
                    if self.direction == 1:
                        newBlockPosX = self.position.x + 1 + (2 * i)
                    else:
                        newBlockPosX = self.position.x - 2 - (2 * i)
                    self.__blocks[-1] = Vector2(newBlockPosX, self.position.y - 1 - 2 * i)
        else:
            # Pone el bloque de escalera correspondiente           
            self.__tablero.setBlock(self.__tablero.getCoord((self.position.x + self.direction, self.position.y)) ,16 if self.direction == 1 else 17)
            self.position.x += self.direction
            self.finish = True
        

    def __drawBlocks(self):
        for i in range(len(self.__blocks)):
            pyxel.rect(self.__blocks[i].x,self.__blocks[i].y,2,2,12)
