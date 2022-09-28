import pyxel
from LevelManager import Level
from EndLevelScreen import EndLevelScreen
from LemmingBehaviour import Lemming
from Tools import Tools
from Tablero import Tablero
from Vector2 import Vector2

class GameMain:

    def __init__(self):
        self.__gameState = 0
        self.__level = Level()
        self.__gameSpeedTimer = 0
        self.start(0)

        # Si se pulsa la G puedes navegar por los niveles usando B y N, además de herramientas prácticamente ilimitadas
        self.__GodMode = False

    @property
    def gameState(self) -> int:
        """ 0: jugando nivel
            1: puntuaciones del nivel"""
        return self.__gameState
    @property
    def level(self):
        return self.__level

    def start(self,level:int):
        """Comienza un nuevo nivel reseteando todas las variables necesarias"""

        self.__level_frame_count = 1
        self.__gameSpeedTimer = -1000
        self.__gameSpeed = 1

        self.__lemmings = []
        # Tumbas
        self.__graves = []
        
        self.__level.loadLevel(level)

        self.__tablero = Tablero(self.__level.level_map,self.__lemmings)
        self.__tools = Tools(self.__tablero,self.__level)
        self.__endLevelScreen = EndLevelScreen(self.__level)

    def update(self):
        if pyxel.frame_count % 2 == 0 and self.__level_frame_count % 2 != 0:
            self.__level_frame_count += 1

        if self.__gameState == 0:
            if self.__level.current_lemmings == 0:
                self.__gameState = 1
            else:
                self.__tools.update()

                self.__spawn_lemmings()

                # Ejecuta update tantas veces como indica gameSpeed
                if self.__level_frame_count % (3 - self.__gameSpeed) == 0:
                    self.__update_lemmings()
                
                self.__save_lemmings()
                self.__kill_lemmings()
                
                # R para reiniciar el nivel
                if pyxel.btnp(pyxel.KEY_R):
                    self.start(self.__level.id)

                # Velocidad del juego
                if pyxel.btnp(pyxel.KEY_RIGHT):
                    self.__gameSpeed = 2
                    self.__gameSpeedTimer = self.__level_frame_count
                if pyxel.btnp(pyxel.KEY_LEFT):
                    self.__gameSpeed = 1
                    self.__gameSpeedTimer = self.__level_frame_count
        
        # Ventana de información de final de nivel
        elif self.__gameState == 1:
            # Una vez termina la ventana reinicia el nivel o pasa al siguiente
             if self.__endLevelScreen.finish:
                self.__gameState = 0
                # Siguiente nivel
                if self.__level.enoughLemmings():     
                    self.start(self.__level.id + 1)
                else:
                # Reinicia el nivel
                    self.start(self.__level.id)

        #GodMode
        if pyxel.btnp(pyxel.KEY_G):
            self.__GodMode = not self.__GodMode
                            
        if self.__GodMode:
            self.__level.limit_items = (99,99,99,99)
            if pyxel.btnp(pyxel.KEY_W):
                self.__level.saved_lemmings = self.__level.start_lemmings
                self.__gameState = 1
            if self.__level.id > 0 and pyxel.btnp(pyxel.KEY_B):                
                self.start(self.__level.id - 1)
            if pyxel.btnp(pyxel.KEY_N):
                self.start(self.__level.id + 1)

        self.__level_frame_count += 1

    def draw(self):
        if self.__gameState == 0:
            pyxel.cls(6)
            self.__info_window()

            self.__tablero.draw()
            self.__draw_graves()
            self.__draw_lemmings()

            self.__tools.draw()

            self.__drawGameSpeed()

        elif self.__gameState == 1:

            if self.__level.saved_lemmings == 0:
                self.__endLevelScreen.drawAllDead()
            else:
                self.__endLevelScreen.draw()    

        if self.__GodMode:
            pyxel.rect(196,240,100,20,0)
            pyxel.text(200,244,"GodMode ON",8)
    
    def __drawGameSpeed(self):
        """Icono que muestra la velocidad del juego"""
        if self.__level_frame_count - self.__gameSpeedTimer < 60:
            pyxel.blt(120,120,2,16 if self.__gameSpeed == 1 else 32,32,16,16,1)

    #region Lemmings
    def __update_lemmings(self):
        """Actualiza el método update de los lemmings"""
        for lemming in self.__lemmings:
            lemming.update(self.__gameSpeed)

    def __draw_lemmings(self):
        """Actualiza el método draw de los lemmings"""
        for lemming in self.__lemmings:
            lemming.draw_lemming(self.__gameSpeed)

    def __spawn_lemmings(self):
        """Spawnea los lemmings"""
        spawnRate = 60
        if self.__level_frame_count % (spawnRate if self.__gameSpeed == 1 else spawnRate / 2) == 0:
            if len(self.__lemmings) == 0:
                self.__tablero.setBlock(self.__level.spawnPosition,11)

            if len(self.__lemmings) < self.__level.current_lemmings:
                self.__lemmings.append(Lemming(self.__tablero))
                pos = self.__tablero.getScreenCoord(self.__level.spawnPosition)                
                pos += (8,4)
                self.__lemmings[-1].position = pos
                
    def __kill_lemmings(self):
        """Matar lemmings muajajajjajaja"""
        # Si un lemming muere, dibuja una tumba en su posición y quita el lemming de la lista de lemmings
        for lemming in self.__lemmings:
            if not lemming.isAlive():
                self.__lemmings.remove(lemming)
                self.__level.current_lemmings -= 1
                if lemming.position not in self.__graves:
                    self.__graves.append(lemming.position-(8,15))

    def __save_lemmings(self):
        """Abre la puerta cuando el primer lemming llega, y actualiza el contador"""
        for lemming in self.__lemmings:
            if lemming.saved:
                if self.__level.saved_lemmings == 0:
                    self.__tablero.setBlock(self.__level.finishPosition,9)
                self.__level.saved_lemmings += 1
                self.__level.current_lemmings -= 1
                self.__lemmings.remove(lemming)

    def __draw_graves(self):
        """Dibuja las tumbas"""
        for grave in self.__graves:
            pyxel.blt(grave.x,grave.y,1,3*16,0,16,16,0)
    #endregion

    def __info_window(self):
        """Información del nivel"""
        muertos = self.__level.start_lemmings - self.__level.current_lemmings - self.__level.saved_lemmings
        currentLimit = []
        for i in range(len(self.__level.limit_items)):
            currentLimit.append(self.__level.limit_items[i] - self.__level.current_items[i])
        paraguas,bloqueadores,escaleras,palas = currentLimit

        pyxel.text(2,5, self.__info_text("Nivel",self.__level.id+1)+
        self.__info_text("Salvados",self.__level.saved_lemmings)+
        self.__info_text("Muertos",muertos) + self.__info_text("Vivos",self.__level.current_lemmings),
        2)
        pyxel.text(2,20,
        self.__info_text("Escaleras:",escaleras,3)+
        self.__info_text("Paraguas",paraguas,3) +
        self.__info_text("Bloqueadores",bloqueadores,3)+
        self.__info_text("Palas",palas,3),
        2)

    def __info_text(self,itemText,itemValue,space = 6):
        return itemText+" "+str(itemValue)+(" "*space if len(str(itemValue)) > 1 else " "*(space + 1))