import random

class MapCreator:
    def createMap(self) -> list:
        """Esta función se encarga de crear niveles aleatorios que luego utilizará la clase LevelManager"""

        board = [[0 for _ in range(14)] for __ in range(16)]
        platforms = 7

        # Laterales con bloques
        for i in range(len(board)):
            for j in range(len(board[i])):
                if i in (0, len(board)-1) or j in (0, len(board[i])-1):
                    board[i][j] = 1

        # Rellenar plataformas
        plats = [0]
        for _ in range(platforms):
            u = 0
            while u in plats: # Evitar que se repita la plataforma
                u = random.randint(1, len(board[:][0])-3) # Fila de la plataforma
            plats.append(u)

            n = random.randint(5 ,10) # Tamaño de la plataforma

            v = random.randint(1, len(board[:][u][1:-2]) - n + 3)

            for x in range(v, v+n+1):
                board[x][u] = 1

        for i in (1,-2):
            board[i][1:-2] = self.changeIn(board[i][1:-2], 1, 2)

        builded = False
        x=1
        while not builded:
            for i in range(len(board[:][x])):
                if not builded:
                    if board[i][x] == 0 and board[i][x+1] == 0 and board[i][x+2] in (1,2) and board[i+1][x+2]:
                        builded = True
                        board[i][x] = 10
                    elif board[i][x] == 0 and board[i][x+1] in (1,2) and board[i+1][x+1]:
                        builded = True
                        board[i][x] = 10

            x += 1

        builded = False
        x=-2
        while not builded:
            for i in range(len(board[:][x])-1, 0, -1):
                if not builded:
                    if board[i][x] == 0:
                        builded = True
                        board[i][x] = 8

            x -= 1

        return board


    def changeIn(self,lista, x, y):
        """ Cambia x por y en la lista """
        list1 = []
        for l in lista: list1.append(l if l != x else y)

        return list1
