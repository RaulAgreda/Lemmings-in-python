from Vector2 import Vector2
import pyxel

class UI_Text_Button:
    def __init__(self,pos:Vector2,text: str,colors = (7,10,8)):
        """@param mousePos: referencia de la posición del ratón\n
        @param colors: colores en orden de (normal, cursor encima, botón presionado)"""
        self.position = pos
        self.size = 0
        self.text = text
        

        self.__colors = colors

        # 0: Nada, 1: cursor encima del botón, 2: presionado, 3:soltado
        self.__buttonState = 0

    @property
    def text(self):
        return self.__text
    @text.setter
    def text(self,text):
        self.__text = text
        self.size = self.__calculateSize()

    @property
    def __mousePos(self):
        return Vector2(pyxel.mouse_x,pyxel.mouse_y)

    def isPressed(self):
        """Si el botón se mantiene presionado"""
        self.__updateButtonState()
        return self.__buttonState == 2

    def pressedUp(self):
        """Si se suelta el botón"""
        self.__updateButtonState()
        return self.__buttonState == 3

    def __updateButtonState(self):
        """Actualiza el estado del botón"""
        if self.__onButton():
            if self.__buttonState != 2:
                self.__buttonState = 1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.__buttonState = 2
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.__buttonState == 2:
                    self.__buttonState = 3
        else:
            self.__buttonState = 0

    def __calculateSize(self) -> Vector2:
        """Longitud del botón"""
        return Vector2(4 * len(self.text),8)

    def __onButton(self) -> bool:
        """Devuelve True si el ratón está encima del botón"""
        diff = self.__mousePos-self.position
        # print(diff)
        return abs(diff.x) < self.size.x/2 and abs(diff.y) < self.size.y/2


    def draw(self):
        """Dibuja el botón, siempre debe ejecutarse después de cualquier función o propiedad de esta clase"""
        color = self.__colors[0]
        if self.__onButton():
            if self.isPressed():
                color = self.__colors[2]
            else:
                color = self.__colors[1]

        pyxel.text(*(self.position - Vector2(self.size.x//2,2)).asTuple(),self.text,color)


class UI_Icon_Switch:
    def __init__(self,pos: Vector2,id:tuple,initState = True):
        """
        \n@param id: 
        \n(id_1,id_2)
        """
        self.position = pos
        self.id = id

        self.__on = initState

    @property
    def __mousePos(self):
        return Vector2(pyxel.mouse_x,pyxel.mouse_y)

    @property
    def on(self):
        """Devuelve el estado del botón on/off <=> True/False"""        
        return self.__on
    
    def onChangeEvent(self):
        """Devuelve el momento en el que el botón cambia de estado"""
        if self.__onButton() and pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.__on = not self.__on
            return True
        return False

    def __onButton(self) -> bool:
        """Devuelve True si el ratón está encima del botón"""
        diff = self.__mousePos-(self.position + (8,8))
        return abs(diff.x) < 8 and abs(diff.y) < 8
    
    def draw(self):
        """Dibuja el botón, siempre debe ejecutarse después de cualquier función o propiedad de esta clase"""
        # print(self.__mousePos,self.__onButton)
        id = self.id[0] if self.__on else self.id[1]
        pyxel.blt(*self.position.asTuple(),2,id%4*16,id//4*16,16,16)
                