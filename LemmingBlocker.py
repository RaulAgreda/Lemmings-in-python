import pyxel
from GameObject import GameObject

class LemmingBlocker(GameObject):
    
    def __init__(self,tablero,startPosition):
        super().__init__()
        self.position = startPosition
        self.__tablero = tablero
        self.finish = False

    def update(self,game_speed):
        # Dibuja la animación del lemming mediante un bloque del tablero
        self.__tablero.setBlock(self.__tablero.getCoord(self.position),20 + int(pyxel.frame_count // (8/game_speed) % 4))
    
    def freeLemming(self):
        """Libera al lemming volviendo a su estado normal"""
        if self.direction != 0:
            self.__tablero.setBlock(self.__tablero.getCoord(self.position),0)
            self.finish = True

    # Esta función es necesaria porque todas las clases de lemming contienen la función update, y la función draw_lemming
    def draw_lemming(self,game_speed):
        pass
