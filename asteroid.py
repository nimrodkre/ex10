from game_piece import GamePiece
import math


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
            raise ValueError("Asteroid size between 1 and 3")

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
