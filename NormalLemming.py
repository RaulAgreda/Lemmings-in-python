from GameObject import GameObject
import pyxel
from SoundSystem import SoundSystem
# from Tablero import Tablero

class NormalLemming(GameObject):  
    def __init__(self,tablero):
        super().__init__()

        self.lemmingState = 0
        
        self.alive = True

        self.__sound = SoundSystem()

        self.__tablero = tablero    
        self.__startFallPosition = 0
    
    @property
    def lemmingState(self):
        return self.__lemmingState

    @lemmingState.setter
    def lemmingState(self,value):
        """
        0: andando
        1: cayendo
        2: cayendo con paraguas
        3: escalera encontrada
        4: subiendo una escalera
        5: bajando una escalera
        """       
        if 0 <= value <= 5:
            self.__lemmingState = value
        else:
            raise ValueError("Debes dar un valor entre [0, 5]")

    def update(self,game_speed):

        self.__controlStates()
        # Aquí se ejecuta cada función según el estado del lemming además de poner la animación adecuada
        # Lemming andando
        if self.lemmingState == 0:
            #Si encuentra pinchos se muere directamente
            if self.__tablero.getBlock(self.position,True) in (24,25,26,27):
                self.alive = False
                self.__sound.play(self.__sound.die_sound)
                return
            self.__move()
            self.id = 0 if self.direction == 1 else 1  

        # Lemming en uno de los estados de caída
        elif self.lemmingState in (1,2):
            self.__fall()
            if self.lemmingState == 1:
                self.id = 2 if self.direction == 1 else 3
            elif self.lemmingState == 2:
                self.id = 4 if self.direction == 1 else 5
        
        # Lemming subiendo escaleras
        elif self.lemmingState in (3,4,5):
            self.__climbStairs()
            self.id = 0 if self.direction == 1 else 1             
            
            
    def draw_lemming(self,game_speed):
        self.draw(pyxel.frame_count*(game_speed/2)//4)   

    def getItem(self) -> int:
        """Comprueba si hay un item de bloqueo, escaleras o la puerta y devuelve:
        0 si no ha cogido nada
        1 si es escalera
        2 si es bloqueo
        3 si es la puerta de salida
        4 si es un bloque para cavar"""

        current_block = self.__tablero.getBlock(self.position,True)
        block_below = self.__tablero.getBlock(self.position,True,(0,1))

        item = 0
        # Id del bloque en el que se enceuntra el Lemming
        if self.lemmingState == 0:
            # Item bloqueo
            if current_block == 6:
                item = 2
            # Item escalera
            elif current_block == 18 and self.direction == 1 or (current_block == 19 and self.direction == -1):
                item = 1
            # Puerta de salida
            elif current_block in (8,9):
                item = 3
            # Bloque para cavar si está en una pared o está debajo y el lemming en el centro del bloque
            elif current_block == 12 or (block_below == 12 and self.__tablero.getRelativeCoord(self.position).x in (6,7,8,9)):
                item = 4         

        return item

    def __controlStates(self):
        """Cambia los estados del lemming"""

        if self.lemmingState == 0:
            #Si se detecta que no tiene ningún bloque debajo, entra en estado de caida
            if self.__isFalling():
                self.__startFallPosition = self.position.y
                self.lemmingState = 1
                self.__sound.play(self.__sound.start_fall_sound)

            #Si encuentra una escalera entra en estado de escalar
            elif self.__checkClimbDirection() in (-1,1):
                self.lemmingState = 3
                # print("Subiendo")

    def __translate(self,direction:tuple or Vector2):
        """Suma a la posición el vector direction"""
        self.position += direction
   
    def __move(self):
        """Mueve automáticamente al lemming en la dirección a la que mira (self.direction)"""

        current_block = self.__tablero.getBlock(self.position,True)     
        blocks = (1,2,12,13,14,15,20,21,22,23)                
        #Si el bloque al que mira es una pared
        if current_block in blocks:    
            self.direction *= -1

        self.__translate((self.direction,0))

    #region caída    
    def __fall(self,fallSpeed = 3):
        """Controla la caída y comprueba la distancia que ha recorrido al empezar a caer para saber si ha muerto o no"""
                
        if self.__isFalling():
            #Cae de forma normal o cae a la mitad de velocidad si tiene un paraguas
            self.__translate((0,fallSpeed if not self.lemmingState == 2 else 1))

            blocks = (1,2,12,13,14,15)
            current_block = self.__tablero.getBlock(self.position,True)

            #Si recoge un paraguas, entra en el estado de caer con paraguas
            if self.lemmingState == 1 and current_block in (4,5):
                self.lemmingState = 2
                self.__sound.play(self.__sound.get_umbrella_sound)
                # Cambia la herramienta de paraguas por el paraguas ineditable, para que una vez usado no se pueda borrar
                self.__tablero.setBlock(self.__tablero.getCoord(self.position),5)

            #Si el lemming está atravesando un bloque, lo teletransporta arriba
            elif current_block in blocks:
                self.position.y = self.position.y - (self.__tablero.getRelativeCoord(self.position).y + 1)
        else:
            #Si cae más de dos bloques muere a no ser que tenga paraguas
            if not self.lemmingState == 2 and abs(self.__startFallPosition - self.position.y) // self.__tablero.SIZE > 2:
                self.alive = False
                self.__sound.play(self.__sound.die_sound)
            else:
            #Si cae sin matarse vuelve al estado de moverse
                self.lemmingState = 0
                # self.__sound.play(self.__sound.fall_sound)

    def __isFalling(self)-> bool:
        """Comprueba si el Lemming se está cayendo"""

        current_block = self.__tablero.getBlock(self.position,True)
        block_below = self.__tablero.getBlock(self.position,True,(0,1))

        y_block_coord = self.__tablero.getRelativeCoord(self.position).y     
        blocks = (1,2,12,13,14,15)

        # Cae si no encuentra bloques colisionables debajo o no está en el suelo (coordenada y == 15 es el suelo) o si está subiendo/bajando una escalera
        return (block_below not in blocks or y_block_coord < self.__tablero.SIZE-1) and current_block not in blocks and self.__checkClimbDirection() == 0
    #endregion

    
    #region subir/bajar escaleras
    def __checkClimbDirection(self):
        """Devuelve:
         1 si encuentra una escalera de subida
        -1 si encuentra una escalera de bajada
         0 si no encuentra escalera o no está en la dirección correcta"""
        current_block = self.__tablero.getBlock(self.position,True)
        block_below = self.__tablero.getBlock(self.position,True,(0,1))
        rel_coord = self.__tablero.getRelativeCoord(self.position)
        dir = 0

        if rel_coord.y == self.__tablero.SIZE - 1:
            # Solo sube la escalera si está en el extremo del bloque y en la dirección correcta
            if (current_block == 16 and self.direction == 1 and rel_coord.x == 0) or (current_block == 17 and self.direction == -1 and rel_coord.x == self.__tablero.SIZE - 1):
                dir = 1
            elif (block_below == 16 and self.direction == -1 and rel_coord.x == self.__tablero.SIZE) or (block_below == 17 and self.direction == 1 and rel_coord.x == 0):
                dir = -1
        return dir

    def __climbStairs(self):
        # 1 subir, -1 bajar
        climbDirection = 0

        current_block = self.__tablero.getBlock(self.position,True)
        block_below = self.__tablero.getBlock(self.position,True,(0,1))

        relativePosition = self.__tablero.getRelativeCoord(self.position)

        if self.lemmingState == 3:
            #Si encuentra una escalera de subida
            if self.__checkClimbDirection() == 1:
                self.lemmingState = 4

            #Si encuentra una escalera de bajada
            elif self.__checkClimbDirection() == -1:
                self.lemmingState = 5

        #Si está subiendo
        if self.lemmingState == 4:
            climbDirection = -1

            #Si ha terminado de subir
            if relativePosition.y == self.__tablero.SIZE-1 and current_block not in (16,17) and self.__tablero.getBlock(self.position,True,(self.direction,-1)) not in (16,17):
                climbDirection = 0
            
        #Si está bajando
        elif self.lemmingState == 5:
            climbDirection = 1

            #Si ha terminado de bajar
            if relativePosition.y == self.__tablero.SIZE - 1 and block_below not in (16,17):
                climbDirection = 0
           
        #Si clibmDirection es 0 vuelve al estado de andar
        if climbDirection == 0:
            self.lemmingState = 0
        else:
            self.__translate((self.direction,climbDirection))
    #endregion