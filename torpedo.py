from game_piece import GamePiece


class Torpedo(GamePiece):
    def __init__(self, x, y, degrees, speed_x, speed_y):
        GamePiece.__init__(self, x, y, speed_x, speed_y)
        self.__degrees = degrees
        self.__radius = 4
        self.__life = 0

    @property
    def degrees(self):
        return self.__degrees

    @degrees.setter
    def degrees(self, degrees):
        self.__degrees = degrees

    @property
    def radius(self):
        return self.__radius

    @property
    def life(self):
        return self.__life

    def increase_life(self):
        self.__life += 1
