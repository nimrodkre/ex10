class Torpedo:
    def __init__(self, x, y, degrees):
        self.__x = x
        self.__y = y
        self.__degrees = degrees

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def degrees(self):
        return self.__degrees

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    @degrees.setter
    def degrees(self, degrees):
        self.__degrees = degrees
