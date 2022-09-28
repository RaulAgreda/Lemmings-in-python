import pyxel
from Vector2 import Vector2

class Tablero:
    def __init__(self, newBoard, lemmingsList ,size: int = 16,offset = Vector2(0,32),idSize = 4):
        """@param newBoard: matriz de listas en el que se van a guardar los valores de los bloques,
        el tamaño del tablero dependerá de las dimensiones de esta\n
        @param lemmingsList: referencia de la lista de lemmings para detectar las coordenadas del tablero donde se encuentran\n
        @param size: tamaño de las casillas, 16 píxeles de lado por defecto\n
        @param offset: desplazamiento del tablero desde la esquina superior izquierda\n
        @param idSize: cantidad de dibujos por línea en el archivo .pyxres"""

        self.__SIZE = size

        self.__tablero = self.__tableroCopy(newBoard)

        self.__lemmings = lemmingsList


        self.__idSize = idSize
        self.__offset = offset

    def __tableroCopy(self,matrix):
        """deepCopy de una matriz"""
        newMatrix = []
        for i in range(len(matrix)):
            newMatrix.append([])
            for j in range(len(matrix[i])):
                newMatrix[i].append(matrix[i][j])
        return newMatrix 

    @property 
    def SIZE(self):
        return self.__SIZE

    def draw(self):
        for i in range(len(self.__tablero)):
            for j in range(len(self.__tablero[i])):
                size = self.__SIZE
                pyxel.blt(i*size+self.__offset.x, j*size + self.__offset.y, 1,
                 self.__tablero[i][j] % self.__idSize * size,
                 self.__tablero[i][j] // self.__idSize * size, size, size,0)
     
    def getLemmingAt(self,coord: tuple or Vector2,type: int):
        """
        @param coord: coordenadas de la matriz
        @param type: trabajo del lemming (0:Normal,1:Builder,2:Blocker)\n
        Devuelve el primer Lemming encontrado de dicho tipo, si no lo encuentra devuelve None"""

        for lemming in self.__lemmings:
            if self.getCoord(lemming.position) == coord and lemming.currentJob == type:
                return lemming.job

        return None

    def isCoordInMatrix(self,coord: tuple or Vector2) -> bool:
        """Comprueba si las coordenadas de la matriz existen"""
        coord = Vector2(coord)

        return coord != (-1,-1) and 0 <= coord.x and coord.x < len(self.__tablero) and 0 <= coord.y and coord.y < len(self.__tablero[0])

    def getCoord(self,coord:tuple or Vector2) -> Vector2:
        """Devuelve coordenadas de la pantalla, en coordenadas del tablero"""

        coord = Vector2(coord) - self.__offset
        coord = Vector2(coord.x // self.__SIZE, coord.y // self.__SIZE)

        #Devuelve (-1,-1) si está fuera de la cuadrícula, si no devuelve las correspondientes coordenadas
        return coord if self.isCoordInMatrix(coord) else (-1,-1)

    def getScreenCoord(self,coord: tuple or Vector2) -> Vector2:
        """Devuelve coordenadas de la matriz en coordenadas de la pantalla"""

        coord = Vector2(coord)

        return Vector2(coord.x * self.__SIZE, coord.y * self.__SIZE) + self.__offset

    def getRelativeCoord(self,coord: tuple or Vector2) -> Vector2:
        """
        Devuelve las coordenadas de un punto relativas al bloque del tablero al que pertenece Ej: si SIZE es 16
            -x: [0,15]
            -y: [0,15]
        @param coord: coordenadas en la pantalla"""
        coord = Vector2(coord)
        return Vector2(coord.x % self.__SIZE, coord.y % self.__SIZE)

    def getBlock(self,coord: tuple or Vector2,screenCoord = False,offset = (0,0)) -> int:
        """Devuelve el número del bloque en las coordenadas de la matriz si existen, si no, devuelve None\n
        @param screenCoord: especifica si poner directamente coordenadas de la pantalla y que se transformen en coordenadas de la matriz\n
        @param offset: devuelve el bloque que está a tantos bloques de coord. Ej: offset=(1,0) comprueba el bloque a la derecha de coord"""
        if screenCoord: coord = self.getCoord(coord)
        else: coord = Vector2(coord)

        if offset != (0,0): coord += offset
        return self.__tablero[coord.x][coord.y] if self.isCoordInMatrix(coord) else None

    def setBlock(self,coord:tuple or Vector2,blockId:int,screenCoord = False):
        """Pone en coordenadas de la cuadrícula el bloque elegido"""
        if screenCoord: coord = self.getCoord(coord)
        else: coord = Vector2(coord)
        if coord != (-1,-1) and self.isCoordInMatrix(coord):
            self.__tablero[coord.x][coord.y] = blockId                   