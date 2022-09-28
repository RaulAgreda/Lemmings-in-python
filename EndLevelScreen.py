import pyxel
from Vector2 import Vector2
from UI_Button import UI_Text_Button

class EndLevelScreen:
    def __init__(self,level,screenTime = 5):
        self.__level = level
        self.__screenTime = screenTime
        self.__timer = 0
        self.__started = False
        self.__finish = False
        self.nextLevelButton = UI_Text_Button(Vector2(128,220),"NEXT LEVEL")
    @property 
    def finish(self):
        return self.__finish

    def __startTimer(self):
        if not self.__started:
            self.__timer = pyxel.frame_count
            self.__started = True

    def draw(self):

        pyxel.cls(0)
        textCateg = ("Nivel","Salvados","Muertos","Paraguas usados","Bloqueadores usados","Escaleras usadas","Palas usadas")
        text = ""

        for i in range(len(textCateg)):
            
            if i == 0: text = str(self.__level.id+1)
            elif i == 1: text = str(self.__level.saved_lemmings)
            elif i == 2: text = str(self.__level.start_lemmings - self.__level.saved_lemmings)
            else: text = str(self.__level.current_items[i-3])

            pyxel.text(20,20*i+20,textCateg[i]+": "+text,7)

        pyxel.text (20,160,self.__mensajesPersonalizados(),7)
        if not self.__level.enoughLemmings():
            pyxel.text (20,180,"Necesitas salvar al menos a "+str(self.__level.lemmingsNeeded())+" lemmings",7)
        

        if self.nextLevelButton.pressedUp():
            self.__finish = True

        self.nextLevelButton.text = "NEXT LEVEL" if self.__level.enoughLemmings() else "RESTART LEVEL"
        self.nextLevelButton.draw()

    def drawAllDead(self):

        self.__startTimer()

        if pyxel.frame_count - self.__timer < 1 * 60:
            pyxel.cls(0)
            if pyxel.frame_count % 6 == 0:
                self.__drawText(Vector2(128,128),"NO TIENES ALMA",8)
        else:
            self.__finish = True

    def __mensajesPersonalizados(self):
        text = ""
        saved = self.__level.saved_lemmings 
        startL = self.__level.start_lemmings
        if saved == 1:
            text = "Enhorabuena ese lemming no solo ya no tiene amigos\nsino que estan todos muertos"
        elif saved == 2:
            text = "Espero que duermas bien por las noches\nesos dos no creo que lo vuelvan a hacer"
        elif saved < startL // 2 - 2:
            text = "Vaya vaya, alguien no esta muy bien de la cabeza"
        elif saved <= startL // 2 + 2:
            text = "Seleccion natural?????"
        elif saved == startL:
            text = "Ole ole los salvaste a todos :D"
        elif saved == startL - 1:
            text = "Se nos ha ido un grande"
        else:
            text = "Menos un par de patosos que se han matao, no esta mal"
        return text

    def __drawText(self,position:Vector2,text,color = 7):
        """Dibuja un texto pero con sus coordenadas centradas"""
        pyxel.text(position.x-(4*len(text)//2),position.y - 4,text,color)