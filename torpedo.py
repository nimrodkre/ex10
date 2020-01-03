from game_piece import GamePiece

RADIUS = 4
INIT_LIFE = 0


class Torpedo(GamePiece):
    """
    Represents a single torpedo that can be shot from the player's ship
    """

    def __init__(self, x, y, degrees, speed_x, speed_y):
        """
        Creates a torpedo, inherits from GamePiece
        :param degrees: The heading of the game_piece in relation to x axis
        """
        GamePiece.__init__(self, x, y, speed_x, speed_y)
        self.__degrees = degrees
        self.__radius = RADIUS
        self.__life = INIT_LIFE

    @property
    def degrees(self):
        """
        :return: int, current heading of the object
        """
        return self.__degrees

    @property
    def radius(self):
        """
        :return: int, the radius of the torpedo
        """
        return self.__radius

    @property
    def life(self):
        """
        :return: how many game rounds the torpedo has been in the game
        """
        return self.__life

    @degrees.setter
    def degrees(self, degrees):
        self.__degrees = degrees

    def increase_life(self):
        self.__life += 1
