from screen import Screen
import sys
from random import randint
from ship import Ship

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(randint(self.__screen_min_x, self.__screen_max_x),
                           randint(self.__screen_min_y, self.__screen_max_y),
                           0, 0, 0)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again

        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)


    def _game_loop(self):
        self.__screen.draw_ship(self.__ship.x, self.__ship.y, self.__ship.degrees)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
