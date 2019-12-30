from screen import Screen
import sys
from random import randint
from ship import Ship
from asteroid import Asteroid

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroids_amount = asteroids_amount

        self.__ship = Ship(randint(self.__screen_min_x, self.__screen_max_x),
                           randint(self.__screen_min_y, self.__screen_max_y),
                           0, 0, 0)

    def build_game(self):
        self.__asteroids = self.build_asteroids(self.__asteroids_amount)

        for asteroid in self.__asteroids:
            self.__screen.register_asteroid(asteroid, asteroid.size)

    def build_asteroids(self, asteroids_amounts):
        ASTEROID_SIZE = 3
        return [Asteroid(randint(self.__screen_min_x, self.__screen_max_x),
                         randint(self.__screen_min_y, self.__screen_max_y),
                         ASTEROID_SIZE, randint(1, 4), randint(1, 4))
                for i in range(asteroids_amounts)]

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again

        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def move_all_gamepieces(self):
        """
        moves all ships, asteroids, torpedoes
        :return: None
        """
        self.__ship.move(self.__screen_min_x, self.__screen_max_x,
                         self.__screen_min_y, self.__screen_max_y)

        for asteroid in self.__asteroids:
            asteroid.move(self.__screen_min_x, self.__screen_max_x,
                          self.__screen_min_y, self.__screen_max_y)

    def draw_all_gamepieces(self):
        """
        draws all gamepieces, ships, asteroids, torpedoes
        :return: None
        """
        self.__screen.draw_ship(self.__ship.x, self.__ship.y,
                                self.__ship.heading)

        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.x, asteroid.y)

    def ship_asteroid_collision(self):
        """
        checks if there are any intersections with an asteroid or ship
        :return: None
        """
        collided_asteroids = []
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                self.__screen.show_message("Collision", "ship collided with "
                                                        "asteroid")
                self.__screen.remove_life()
                collided_asteroids.append(asteroid)

        # remove all collided asteroids
        for asteroid in collided_asteroids:
            self.__screen.unregister_asteroid(asteroid)
            self.__asteroids.remove(asteroid)


    def _game_loop(self):
        self.draw_all_gamepieces()
        self.move_all_gamepieces()
        self.ship_asteroid_collision()

        if self.__screen.is_left_pressed():
            self.__ship.change_heading(1)
        if self.__screen.is_right_pressed():
            self.__ship.change_heading(0)
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()


def main(amount):
    runner = GameRunner(amount)
    runner.build_game()
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
