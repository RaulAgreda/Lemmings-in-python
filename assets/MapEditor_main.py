import pyxel
from MapEditor_tablero import Tablero

start = False
def update():
    global start

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    if not start:
        tablero.tablero = LoadMap()
    start = True
    
    if pyxel.btnp(pyxel.KEY_P):
        matrix = tablero.tablero
        for i in range(len(matrix)):
            print(("(" if i == 0 else "") + str(tuple(matrix[i])) + ("," if i < len(matrix) - 1 else ")\n"))
        
def LoadMap():
    map_here =    ((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 10, 0, 0, 1, 1, 0, 24, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 26, 1),
        (1, 0, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1, 0, 1),
        (1, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 1, 1, 2, 24, 1, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 8, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
    map_loaded = []
    for i in map_here:
        map_loaded.append(list(i))
    return map_loaded

def draw():   
    pyxel.cls(6)
    tablero.draw()
    draw_map()


blockType = 0   
def draw_map():
    global blockType
    buildingBlocks = (1,2,8,10,16,17,24,25,26,27)
    
    
    # print(pyxel.mouse_wheel)
    if pyxel.mouse_wheel > 0 or pyxel.btnp(pyxel.KEY_UP):
        blockType = blockType + 1 if blockType < len(buildingBlocks) - 1 else 0
    elif pyxel.mouse_wheel < 0 or pyxel.btnp(pyxel.KEY_DOWN):
        blockType = blockType - 1 if blockType > 0 else len(buildingBlocks) - 1
  
    if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
    # print(tablero.getCoord((pyxel.mouse_x,pyxel.mouse_y)))
        tablero.setBlock(tablero.getCoord((pyxel.mouse_x,pyxel.mouse_y)), buildingBlocks[blockType])
    if pyxel.btn(pyxel.MOUSE_RIGHT_BUTTON):
        tablero.setBlock(tablero.getCoord((pyxel.mouse_x,pyxel.mouse_y)), 0)

################## main program ##################


WIDTH = 256
HEIGHT = 256
CAPTION = "Lemmings by Danifdzzzz and RaxerXD"

# The first thing to do is to create the screen, see API for more parameters
pyxel.init(WIDTH, HEIGHT, caption = CAPTION,scale = pyxel.DEFAULT_SCALE, palette = pyxel.DEFAULT_PALETTE,fps = 60)

#Load images
pyxel.load("my_resource.pyxres")

tablero = Tablero()

pyxel.mouse(True)
# To start the game we invoke the run method with the update and draw functions
pyxel.run(update, draw)