from MapCreator import MapCreator
import random

class Level():
    """Esta clase se encarga de cargar los niveles, los primeros son los índices de los
    mapas prestablecidos, a partir de ahí todos los niveles se generan de forma aleatoria"""
    def __init__(self):    
        # Se guarda el nivel random por si hay que reiniciarlo    
        self.__currentRandomLevel = None      
  
    # Variables solo de lectura
    @property
    def level_map(self):
        return self.__level_map
    @property
    def spawnPosition(self):
        return self.__spawnPosition
    @property
    def finishPosition(self):
        return self.__finishPosition

    def loadLevel(self,level_id):
        self.id = level_id

        isRandom = LoadMap.getAtributes(level_id) == None

        self.current_items = [0,0,0,0]
        self.saved_lemmings = 0

        if isRandom:
            # Si la id es la misma y el mapa era random, se restablece el mismo mapa random
            if self.__currentRandomLevel != None and self.__currentRandomLevel[-1] == level_id:
                self.__reloadCurrentRandomLevel()
            # Si no, se genera uno nuevo
            else:
                self.__level_map = MapCreator().createMap()
                self.limit_items = tuple([5 for _ in range(len(self.current_items))])
                self.start_lemmings = random.randint(10,20)
                self.current_lemmings = self.start_lemmings
                self.savePercentage = 75
                self.__currentRandomLevel = self.__getCurrentRandomLevel()
        else:
            self.__level_map = LoadMap.getMap(level_id)

            levelAtrib = LoadMap.getAtributes(level_id)
            self.limit_items = levelAtrib[:-2]
            self.start_lemmings = self.current_lemmings = levelAtrib[-2]
            self.savePercentage = levelAtrib[-1]

        # Trampilla
        self.__spawnPosition = (0,0)
        # Puerta
        self.__finishPosition = (0,0)
        self.__set_Spawn_Finish_Coord()

    def enoughLemmings(self):
        """Devuelve True si se han salvado suficientes lemmings para pasar de nivel"""
        return self.saved_lemmings >= self.lemmingsNeeded()

    def lemmingsNeeded(self):
        """Devuelve el número de lemmings que se necesitan para pasar de nivel"""
        return int(self.start_lemmings * (self.savePercentage/100))

    def __reloadCurrentRandomLevel(self):
        self.__level_map,self.start_lemmings,self.id = self.__currentRandomLevel
        self.current_lemmings = self.start_lemmings

    def __getCurrentRandomLevel(self):
        """Devuelve una tupla con (level_map,start_lemmings,id)"""
        mapCopy = []
        for i in range(len(self.__level_map)):
            mapCopy.append([])
            for j in range(len(self.__level_map[i])):
                mapCopy[i].append(self.__level_map[i][j])
            mapCopy[i] = list(mapCopy[i])

        return list(mapCopy),self.start_lemmings,self.id

    def __set_Spawn_Finish_Coord(self):
        """Inicializa las variables spawnPosition y finishPosition en coordenadas del mapa de la matriz
        buscando la trampilla de entrada y la puerta de salida"""     
        for i in range(len(self.__level_map)):
            if 10 in self.__level_map[i]:
                j = self.__level_map[i].index(10)
                self.__spawnPosition = (i,j)

            if 8 in self.__level_map[i]:
                j = self.__level_map[i].index(8)
                self.__finishPosition = (i,j)

class LoadMap:

    def getAtributes(level:int):
        """Devuelve los atributos de cada mapa"""
        # paraguas/bloqueadores/escaleras/palas/número de lemmings/porcentaje de lemmings que hay que salvar
        levels = (
        (1,0,1,0,10,60),
        (1,0,4,0,10,80),
        (1,1,1,1,10,80),
        (10,10,10,10,10,80),
        (3,2,5,5,20,70),
        (0,2,15,3,10,70)
        )

        return levels[level] if level < len(levels) else None

    def getMap(level:int):
        """Devuelve la copia de un mapa prefabricado"""
        
        # Aquí copiamos la matriz de los diferentes mapas
        maps = (
        ((1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1),
        (1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2),
        (1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2),
        (1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 2, 1, 2, 2, 2, 1, 10, 0, 1, 0, 0, 0, 1),
        (2, 1, 2, 2, 2, 2, 1, 0, 0, 1, 0, 0, 8, 1),
        (1, 1, 1, 2, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1),
        (2, 1, 2, 1, 2, 1, 1, 0, 0, 1, 0, 1, 1, 1),
        (2, 1, 1, 1, 2, 1, 1, 0, 0, 1, 0, 0, 1, 1),
        (2, 1, 2, 1, 2, 1, 1, 0, 0, 1, 0, 0, 1, 1),
        (1, 1, 2, 1, 2, 1, 1, 0, 0, 0, 0, 0, 1, 2),
        (1, 2, 1, 1, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1),
        (1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2),
        (1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1),
        (1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1),
        (1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)), 
        
        ((1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2),
        (1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1),
        (1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1),
        (1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1),
        (1, 2, 1, 1, 0, 8, 1, 2, 2, 1, 1, 2, 1, 1),
        (2, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 2, 1),
        (2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1),
        (1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2),
        (1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2),
        (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2),
        (1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1, 2, 1),
        (1, 1, 2, 1, 1, 1, 1, 10, 0, 1, 1, 1, 2, 1),
        (1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1),
        (1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1),
        (1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2),
        (1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1)),
        
        ((1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1),
        (2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2),
        (2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1),
        (1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 24, 1),
        (2, 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1),
        (2, 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1),
        (1, 2, 1, 2, 1, 0, 1, 1, 0, 0, 1, 2, 2, 1),
        (1, 2, 1, 2, 1, 0, 0, 1, 0, 0, 1, 2, 2, 2),
        (1, 2, 1, 1, 1, 2, 2, 1, 0, 0, 1, 1, 1, 2),
        (1, 1, 2, 1, 1, 0, 0, 1, 0, 8, 1, 1, 1, 2),
        (1, 1, 2, 1, 1, 10, 0, 1, 0, 0, 1, 1, 1, 2),
        (1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2),
        (1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2),
        (1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1),
        (1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1)),
        ((1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1),

        (1, 10, 0, 1, 1, 2, 2, 1, 1, 0, 0, 0, 8, 1),
        (1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 24, 1),
        (1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1),
        (1, 2, 2, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1),
        (1, 0, 0, 2, 0, 1, 0, 1, 2, 1, 0, 0, 1, 1),
        (1, 0, 0, 1, 0, 1, 0, 1, 1, 2, 2, 0, 1, 1),
        (1, 0, 0, 1, 0, 1, 0, 2, 2, 2, 1, 0, 1, 1),
        (1, 0, 0, 2, 0, 1, 0, 2, 2, 1, 1, 0, 1, 1),
        (1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1),
        (1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1),
        (1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1),
        (1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1),
        (1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
        (1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)),

        ((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
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
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)),

        ((1, 1, 1, 1, 1, 26, 1, 1, 1, 1, 1, 1, 1, 2),
        (1, 0, 8, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1),
        (1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 1, 1),
        (1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 1),
        (1, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 1),
        (1, 0, 0, 0, 0, 24, 1, 10, 0, 1, 1, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1),
        (1, 2, 2, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1),
        (1, 2, 1, 1, 25, 0, 0, 0, 0, 0, 0, 1, 1, 2),
        (1, 1, 1, 25, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2),
        (1, 1, 1, 25, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2),
        (1, 1, 1, 25, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))     
        )

        return maps[level] if level < len(maps) else None