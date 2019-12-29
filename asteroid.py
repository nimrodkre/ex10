from game_piece import GamePiece

class Asteroid(GamePiece):
    def __init__(self, x, y, size, speed_x, speed_y):
        GamePiece.__init__(self, x, y, speed_x, speed_y)
        self.__size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        if type(size) != int:
            raise TypeError("Expected int")
        if size < 1 or size > 3:
            raise ValueError("Torpedo size between 1 and 3")

        self.__size = size
