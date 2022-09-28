import pyxel

class Tablero:
    def __init__(self,x = 16, y = 14):
        #Longitud columnas de la matriz
        self.x = x
        #Longitud filas de la matriz
        self.y = y

        #Inicializa el tablero como una matriz de ceros
        self.tablero = []
        for _ in range(x):
            self.tablero.append([0]*y)


    def draw(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                pyxel.blt(i*16,j*16 + 16*2,1,self.tablero[i][j]%4*16,self.tablero[i][j] // 4 * 16,16,16,0)

    def getCoord(self,coord):
        """Devuelve coordenadas de la pantalla, en coordenadas del tablero"""
        coords = (coord[0] // 16, coord[1] // 16 - 2)
        #Devuelve (-1,-1) si está fuera de la cuadrícula, si no devuelve las correspondientes coordenadas
        return coords if (0 <= coords[0] < self.x) and (0 <= coords[1] < self.y) else (-1,-1)

    def setBlock(self,coord:tuple,type:int):
        """Pone en coordenadas de la cuadrícula el bloque elegido"""
        if coord != (-1,-1):
            self.tablero[coord[0]][coord[1]] = type