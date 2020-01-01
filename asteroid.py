from game_piece import GamePiece
import math

MIN_SIZE = 1
MAX_SIZE = 3


class Asteroid(GamePiece):
    def __init__(self, x, y, size, speed_x, speed_y):
        GamePiece.__init__(self, x, y, speed_x, speed_y)
        self.__size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        if isinstance(size, int):
            raise TypeError("Expected int")
        if size < MIN_SIZE or size > MAX_SIZE:
            raise ValueError("Asteroid size between {0} and {1}".format(
                MIN_SIZE, MAX_SIZE))

        self.__size = size

    def calculate_radius(self):
        return self.size * 10 - 5

    def has_intersection(self, obj):
        """
        checks if the given object and the asteroid have collided
        :param obj: the object to check
        :return:
        """
        distance = math.sqrt(math.pow((obj.x - self.x), 2) +
                             math.pow((obj.y - self.y), 2))

        return distance <= self.calculate_radius() + obj.radius
