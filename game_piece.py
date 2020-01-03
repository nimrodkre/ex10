class GamePiece:
    """
    Represent a object in the game that can be placed on the screen and move
    """
    def __init__(self, x, y, speed_x, speed_y):
        """
        Creates a new game piece
        :param x: The initial x location on the screen
        :param y: The initial y location on the screen
        :param speed_x: The initial speed on the x axis
        :param speed_y: initial speed on the y axis
        """
        self.__x = x
        self.__y = y
        self.__speed_x = speed_x
        self.__speed_y = speed_y

    @property
    def x(self):
        """
        The current X location of the game piece
        :return: A float representing the X location on the screen
        """
        return self.__x

    @property
    def y(self):
        """
        The current Y location of the game piece
        :return: A float representing the Y location on the screen
        """
        return self.__y

    @property
    def speed_x(self):
        """
        The current X speed of the game piece
        :return: A float representing the X speed on the screen
        """
        return self.__speed_x

    @property
    def speed_y(self):
        """
        The current Y speed of the game piece
        :return: A float representing the Y speed on the screen
        """
        return self.__speed_y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    @speed_x.setter
    def speed_x(self, speed_x):
        self.__speed_x = speed_x

    @speed_y.setter
    def speed_y(self, speed_y):
        self.__speed_y = speed_y

    def move(self, screen_min_x, screen_max_x, screen_min_y, screen_max_y):
        """
        moves according to the given instructions
        :return: None
        """
        delta_x = screen_max_x - screen_min_x
        delta_y = screen_max_y - screen_min_y

        new_x = screen_min_x + (self.x + self.speed_x - screen_min_x) % delta_x
        new_y = screen_min_y + (self.y + self.speed_y - screen_min_y) % delta_y

        self.x = new_x
        self.y = new_y
