from game_piece import GamePiece

class Ship(GamePiece):
    def __init__(self, x, y, degrees, speed_x, speed_y):
        GamePiece.__init__(self, x, y, speed_x, speed_y)
        self.__degrees = degrees

    @property
    def degrees(self):
        return self.__degrees

    @degrees.setter
    def degrees(self, degrees):
        self.__degrees = degrees
