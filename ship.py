from game_piece import GamePiece
import math

RADIUS = 1
DEGREES_CHANGE = 7
DEGREES_CIRCLE = 360


class Ship(GamePiece):
    def __init__(self, x, y, heading, speed_x, speed_y):
        GamePiece.__init__(self, x, y, speed_x, speed_y)
        self.__heading = heading
        self.__radius = RADIUS

    @property
    def heading(self):
        return self.__heading

    @property
    def radius(self):
        return self.__radius

    @heading.setter
    def heading(self, heading):
        self.__heading = heading
    
    def change_heading(self, side):
        """
        changes the heading of the ship
        :param side: if 0 than right, and change 7 degrees clockwise
                     if 1 than left, and change 7 degrees counter-clockwise
        :return: None
        """
        if side:
            new_heading = (self.heading + DEGREES_CHANGE) % DEGREES_CIRCLE
        else:
            new_heading = (self.heading - DEGREES_CHANGE) % DEGREES_CIRCLE

        self.heading = new_heading

    def accelerate(self):
        """
        accelerates movement of ship
        :return: None
        """
        new_speed_x = self.speed_x + math.cos(math.radians(self.heading))
        new_speed_y = self.speed_y + math.sin(math.radians(self.heading))

        self.speed_x = new_speed_x
        self.speed_y = new_speed_y

