import pyxel
from Vector2 import Vector2

class Tools:
    def __init__(self, tablero, level):

        self.__level = level
        self.__tablero = tablero
        # Menú abierto
        self.__open = False
        # Posición inicial del menú
        self.__menuPos = Vector2(0,0)
        
        """toolSelected=
        -1: martillo
         0: paraguas
         1: bloqueo
         2: escalera derecha
         3: escalera izquierda
        """
        self.__toolSelected = -1

        # Guarda el objeto del lemming bloqueador seleccionado
        self.__blockerSelected = None

        self.__drawArrow = False
    
    @property
    def __mousePos(self):
        return Vector2(pyxel.mouse_x, pyxel.mouse_y)

    def update(self):

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.__openMenu()
        if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
            self.__closeMenu()
        
        self.__selectToolByKey()
        
        self.__buildTool()
        self.__freeBlocker()            

    def draw(self):
        # Dial de herramientas
        if self.__open:
            pyxel.blt(*self.__menuPos.asTuple(), 2, 0, 32, 16, 16, 0) # Martillo
            pyxel.blt(*(self.__menuPos+(0,-20)).asTuple(), 2, 0, 0, 16, 16, 0) # Paraguas
            pyxel.blt(*(self.__menuPos+(0, 20)).asTuple(), 2, 16, 0, 16, 16, 0) # Bloqueo
            pyxel.blt(*(self.__menuPos+(20, 0)).asTuple(), 2, 32, 0, 16, 16, 0) # Escalera derecha
            pyxel.blt(*(self.__menuPos+(-20,0)).asTuple(), 2, 48, 0, 16, 16, 0) # Escalera izquierda

        # Herramienta seleccionada arriba a la derecha
        pyxel.blt(230, 5, 2, 16 * self.__toolSelected if self.__toolSelected != -1 else 0, 0 if self.__toolSelected != -1 else 32, 16, 16, 0)

        # Herramienta seleccionada en el cursor
        self.__drawToolSelected()

        # Flecha que libera al lemming bloqueador
        if self.__blockerSelected != None and self.__drawArrow:
            self.__drawBlockerArrow()

    def __drawToolSelected(self):
        """Dibuja la herramienta seleccionada en la posicón del cursor e indica si se puede colocar o no"""
        toolPos = self.__mousePos - self.__tablero.getRelativeCoord(self.__mousePos)

        if self.__toolSelected != -1 and not pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            pyxel.blt(toolPos.x,toolPos.y,2,self.__toolSelected*16,0 if self.__canBePlaced() else 16,16,16,0)

    def __drawBlockerArrow(self):
        """Dibujo de la flecha que libera al lemming bloqueador"""
        lemmingCoord = self.__blockerSelected.position - self.__tablero.getRelativeCoord(self.__blockerSelected.position) + (8,10)
        direction = self.__blockerSelected.direction
        
        pyxel.line(self.__mousePos.x, lemmingCoord.y, self.__mousePos.x - 8 * direction, lemmingCoord.y + 4, 12)
        pyxel.line(lemmingCoord.x,lemmingCoord.y, self.__mousePos.x, lemmingCoord.y, 12)
        pyxel.line(self.__mousePos.x, lemmingCoord.y, self.__mousePos.x - 8 * direction, lemmingCoord.y - 4, 12)

    def __buildTool(self):
        """Coloca o destruye items según la herramienta seleccionada"""

        # Posición del cursor en la matriz
        tabPos = self.__tablero.getCoord(self.__mousePos)
        tools_tuple = (4,6,18,19,12)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #Construir item
            if self.__toolSelected != -1:
                if self.__canBePlaced():
                    # if self.__level.current_items[self.__toolSelected] < self.__level.limit_items[self.__toolSelected]:
                    self.__tablero.setBlock(tabPos,tools_tuple[self.__toolSelected])
                    self.__addCurrentItem(1,self.__toolSelected)
            # herramienta martillo / colocar palas
            else:
                blockClicked = self.__tablero.getBlock(tabPos)
                # Destruye la herramienta correspondiente sustituyéndolo por un bloque de aire
                if blockClicked in tools_tuple:
                    toolDestroyed = blockClicked
                    self.__tablero.setBlock(tabPos,0 if blockClicked != 12 else 2)
                    self.__addCurrentItem(-1,tools_tuple.index(toolDestroyed))
                # Si hay un bloque de arena, coloca una pala
                elif blockClicked == 2:
                    # print("bloque de arena")
                    if self.__level.current_items[3] < self.__level.limit_items[3]:
                        self.__tablero.setBlock(tabPos,12)
                        self.__addCurrentItem(1,4)   

    def __addCurrentItem(self,cant: int, item: int):
        """Añade o quita cant (puede ser tanto positivo como negativo) al contador del item especificado\n
        @param item: índice de: (paraguas, bloqueadores, escalera derecha, escalera izquierda, palas)"""
        if item in (2,3):
            self.__level.current_items[2] += cant
        elif item == 4:
            self.__level.current_items[3] += cant
        else:
            self.__level.current_items[item] += cant        

    def __freeBlocker(self):
        """Esta función libera a un lemming bloqueador"""

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):

            self.__blockerSelected = self.__tablero.getLemmingAt(self.__tablero.getCoord(self.__mousePos),2)
                
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.__toolSelected == -1:
            if self.__blockerSelected != None:
                # Centra las coordenadas indicando donde se encuentra el lemming
                lemmingCoord = self.__blockerSelected.position - self.__tablero.getRelativeCoord(self.__blockerSelected.position) + (8,10)
                # Según a dónde apunte la flecha establece la dirección a la que mira el Lemming
                self.__blockerSelected.direction = 1 if self.__mousePos.x - lemmingCoord.x > 1 else - 1

                # Dibujo de la flecha
                if abs(self.__mousePos.x - lemmingCoord.x) > 10:
                    self.__drawArrow = True
                else:
                    self.__drawArrow = False
                    self.__blockerSelected.direction = 0
        else:
            if self.__blockerSelected != None:                
                self.__blockerSelected.freeLemming()                 
                self.__blockerSelected = None

    def __canBePlaced(self) -> bool:
        """Devuelve True si se puede construir una herramienta en las coordenadas que indica el cursor"""

        item = self.__toolSelected if self.__toolSelected not in (2,3) else 2

        if self.__level.current_items[item] < self.__level.limit_items[item]:        
            # cursor_tablero = self.__tablero.getCoord(self.__mousePos)
            if self.__tablero.getBlock(self.__mousePos,True) == 0:
                #El paraguas solo se puede poner si hay un bloque de aire debajo
                if self.__toolSelected == 0 and self.__tablero.getBlock(self.__mousePos,True,(0,1)) == 0:
                    return True
                #El bloqueador solo se puede poner si hay un bloque sólido debajo
                elif self.__toolSelected == 1 and self.__tablero.getBlock(self.__mousePos,True,(0,1)) in (1,2):
                    return True
                #La escalera solo se puede poner si arriba hay un bloque de aire
                elif self.__tablero.getBlock(self.__mousePos,True,(0,-1)) == 0 and self.__toolSelected in (2,3):
                    return True

        return False

    def __openMenu(self):
        """Abre el menú de herramientas y guarda la posición donde fue abierto"""
        if not self.__open:
            self.__menuPos = self.__mousePos - Vector2(8,8)
            self.__open = True

    def __closeMenu(self):
        """Cierra el menú seleccionando la herramienta correspondiente"""
        
        vector = self.__mousePos - (self.__menuPos + (8,8))
        selection = 0

        x, y = vector.x,vector.y

        # Mediante la dirección y longitud del vector resultante entre la posición del cursor y la del menú
        # miramos que herramienta selecciona con el ratón
        if abs(x) > abs(y):
            if abs(x) > 10:
                if x > 0:
                    #escalera derecha
                    selection = 2
                else:
                    #escalera izquierda
                    selection = 3
            else:
                # martillo
                selection = -1
        else:
            if abs(y) > 10:
                if y > 0:
                    #prohibido
                    selection = 1
                else:
                    #paraguas
                    selection = 0
            else:
                # martillo
                selection = -1

        self.__toolSelected = selection
        self.__open = False

    def __selectToolByKey(self):
        """Seleccionar la herramienta mediante los números del teclado 
        en vez de con el ratón"""
        selection = self.__toolSelected
        if pyxel.btnp(pyxel.KEY_1):
            selection = 0
        if pyxel.btnp(pyxel.KEY_2):
            selection = 1
        if pyxel.btnp(pyxel.KEY_3):
            selection = 2
        if pyxel.btnp(pyxel.KEY_4):
            selection = 3

        self.__toolSelected = selection
