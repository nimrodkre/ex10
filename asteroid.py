class Asteroid:
    def __init__(self, x, y, speed):
        self.__x = x
        self.__y = y
        self.__speed = speed

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def speed(self):
        return self.__speed

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y

    @speed.setter
    def speed(self, speed):
        if type(speed) != int:
            raise TypeError("Expected int")
        if speed < 1 or speed > 3:
            raise ValueError("Torpedo speed between 1 and 3")

        self.__speed = speed
