import pyxel
from GameManager import GameMain
from Vector2 import Vector2
from UI_Button import UI_Text_Button
from UI_Button import UI_Icon_Switch
from SoundSystem import Music
from NormalLemming import NormalLemming
from Tablero import Tablero
import random

class App:
    def __init__(self):
        self.__lemmingsRain = []
        self.__tablero = Tablero((
        (0, 0, 0, 1),(0, 0, 0, 1),(0, 0, 0, 1),
        (0, 0, 0, 1),(0, 0, 0, 1),(0, 0, 0, 1),
        (0, 0, 0, 1),(0, 1, 0, 1),(0, 1, 0, 1),
        (0, 1, 0, 1),(0, 1, 0, 1),(0, 0, 0, 1),
        (0, 0, 0, 1),(0, 0, 0, 1),(0, 0, 0, 1),
        (0, 0, 0, 1),(0, 0, 0, 1),(0, 0, 0, 1)),
        self.__lemmingsRain,8,Vector2(56,40))
        
        WIDTH = 256
        HEIGHT = 256


        """
		0: pantalla de inicio,
        1: game
        2: abrir menú con los controles del juego y tal
        3: Game Over """
        self.__app_state = 0

        pyxel.init(WIDTH, HEIGHT,fps = 60)

        #Load images
        pyxel.load("assets/my_resource.pyxres")

        self.__game = GameMain()
        self.__music = Music()

        # Botones
        self.__startButton = UI_Text_Button(Vector2(128,100),"START",(3,10,12))
        self.__resumeButton = UI_Text_Button(Vector2(128,80),"RESUME",(7,10,3))
        self.__restartLevelButton = UI_Text_Button(Vector2(128,100),"RESTART LEVEL (R)",(7,10,8))
        self.__exitButton = UI_Text_Button(Vector2(128,180),"EXIT GAME",(8,10,2))

        self.__toggleMusicButton = UI_Icon_Switch(Vector2(120,120),(12,13))

        self.__exitTimer = 0
        self.__stop_level_music = False

        pyxel.mouse(True)

        pyxel.run(self.__update, self.__draw)

    @property 
    def __mousePos(self):
        return Vector2(pyxel.mouse_x,pyxel.mouse_y)

    def __update(self):
        # Menú de inicio
        if self.__app_state == 0:
            if pyxel.frame_count % random.randint(2,120) == 0:
                self.__spawnRandomLemming()
            self.__updateLemmingsRain()

            # Cierra el juego
            if self.__exitButton.pressedUp():
                self.__app_state = 3
                self.__exitTimer = pyxel.frame_count

            if self.__startButton.pressedUp():
                self.__lemmingsRain.clear()     
                self.__app_state = 1
                self.__music.playMusic()

        # Jugando
        elif self.__app_state == 1:     
                           
            self.__game.update() 

            # Abrir menú con la M o la P
            if self.__game.gameState == 0 and (pyxel.btnp(pyxel.KEY_M) or pyxel.btnp(pyxel.KEY_P)):
                self.__app_state = 2

            # Si la música está activada
            if self.__toggleMusicButton.on:
                # Apagar música al final del nivel
                if self.__game.gameState == 1:
                    self.__music.stopMusic()
                    self.__stop_level_music = True
                # Encender música al inicio del nivel
                if self.__stop_level_music and self.__game.gameState == 0:
                    self.__music.playMusic()
                    self.__stop_level_music = False
        
        # Menú del juego
        elif self.__app_state == 2:

            # Vuelve al juego
            if self.__resumeButton.pressedUp() or pyxel.btnp(pyxel.KEY_M) or pyxel.btnp(pyxel.KEY_P):
                self.__app_state = 1

            # Reincia el nivel    
            if self.__restartLevelButton.pressedUp() or pyxel.btnp(pyxel.KEY_R):
                self.__app_state = 1
                self.__game.start(self.__game.level.id)

            # Cierra el juego
            if self.__exitButton.pressedUp():
                self.__app_state = 3
                self.__exitTimer = pyxel.frame_count

            # Enciende y apaga la música
            if self.__toggleMusicButton.onChangeEvent():
                self.__music.playMusic() if self.__toggleMusicButton.on else self.__music.stopMusic()
        
    def __draw(self):
        pyxel.cls(0)
        
        if self.__app_state == 0:    
            # self.__tablero.draw()
            self.__drawLemmingsRain()            
            self.__drawText(Vector2(128,52),"LEMMINGS")
            self.__drawText(Vector2(128,68),"BY RAUL AGREDA AND DANIEL FERNANDEZ")
            self.__startButton.draw()
            self.__exitButton.draw()

        elif self.__app_state == 1:
            self.__game.draw()

        elif self.__app_state == 2:
            self.__drawText(Vector2(128,40),"GAME PAUSED",2)
            self.__drawText(Vector2(128,60),"Debes salvar al menos a "+str(self.__game.level.lemmingsNeeded())+" lemmings",12)
            self.__resumeButton.draw()
            self.__restartLevelButton.draw()
            self.__exitButton.draw()
            self.__toggleMusicButton.draw()
        elif self.__app_state == 3:
            if pyxel.frame_count - self.__exitTimer < 3*60:
                self.__drawText(Vector2(128,128),"GAME OVER",7)
            else:
                pyxel.quit()

    # region Pequeño detalle por rellenar xD
    def __spawnRandomLemming(self):
        self.__lemmingsRain.append(NormalLemming(self.__tablero))
        self.__lemmingsRain[-1].position = Vector2(random.randint(0,256),-16)
        self.__lemmingsRain[-1].direction = -1 if random.randint(0,1) == 0 else 1

    def __updateLemmingsRain(self):
            for lemming in self.__lemmingsRain:
                if pyxel.frame_count % 2 == 0:
                    lemming.update(1)
                if not lemming.alive:
                    lemming.lemmingState = 0
                    lemming.alive = True
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    if self.__mousePos.distance(lemming.position) < 20:
                        lemming.lemmingState = 2
                if lemming.position.y > 270:
                    self.__lemmingsRain.remove(lemming)
                    del(lemming)

    def __drawLemmingsRain(self):
        for lemming in self.__lemmingsRain:
            lemming.draw_lemming(1)
            if lemming.lemmingState == 1 and self.__mousePos.distance(lemming.position) < 20:
                pyxel.blt(*(self.__mousePos + (-8,-16)).asTuple(),1,0,16,16,16,0)
    #endregion

    def __drawText(self,position:Vector2,text,color = 7):
        """Dibuja un texto pero con sus coordenadas centradas"""
        pyxel.text(position.x-(4*len(text)//2),position.y - 4,text,color)


App()
