import pyxel

class SoundSystem:
    def __init__(self):
        # (banco,sonido)
        # El banco 0 es para los sonidos de movimiento y el 1 para cuando cogen un item
        self.__die_sound = (0,0)
        self.__fall_sound = (0,1)      
        self.__build_sound = (1,2)
        self.__get_umbrella = (1,3)
        self.__enter_door_sound = (1,4)
        self.__dig_sound = (1,5)
        self.__start_fall_sound = (0,6)
        self.__block_sound = (1,7)

    @property
    def die_sound(self):
        return self.__die_sound
    @property
    def fall_sound(self):
        return self.__fall_sound
    @property
    def build_sound(self):
        return self.__build_sound
    @property
    def get_umbrella_sound(self):
        return self.__get_umbrella
    @property
    def enter_door_sound(self):
        return self.__enter_door_sound
    @property
    def dig_sound(self):
        return self.__dig_sound
    @property
    def start_fall_sound(self):
        return self.__start_fall_sound
    @property
    def block_sound(self):
        return self.__block_sound

    def play(self,sound):
        pyxel.play(*sound)

class Music:
    def __init__(self):
        pyxel.sound(20).set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "p",
            "2",
            "vffn fnff vffs vfnn",
            25,
            )

        pyxel.sound(21).set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
            "s",
            "2",
            "nnff vfff vvvv vfff svff vfff vvvv svnn",
            25,
        )

        pyxel.sound(22).set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1" "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t",
            "2",
            "n",
            25,
        )

        pyxel.sound(23).set(
            "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1" "f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
            "t",
            "2",
            "n",
            25,
        )

    def playMusic(self):
        pyxel.play(2, [20, 21], loop=True)
        pyxel.play(3, [22, 23], loop=True)
    
    def stopMusic(self):
        pyxel.stop(2)
        pyxel.stop(3)