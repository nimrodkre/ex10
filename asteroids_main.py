import math

from screen import Screen
import sys
from random import randint
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo

DEFAULT_ASTEROIDS_NUM = 5
SCORE_TABLE = {
    3: 20,
    2: 50,
    1: 100
}
MAX_TORPEDO_NUM = 10
MAX_TORPEDO_LIFE = 200


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroids_amount = asteroids_amount

        self.__ship = None
        self.__asteroids = None
        self.__torpedoes = []
        self.__score = 0

    def build_game(self):
        self.__ship = Ship(randint(self.__screen_min_x, self.__screen_max_x),
                           randint(self.__screen_min_y, self.__screen_max_y),
                           0, 0, 0)

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

        for torpedo in self.__torpedoes:
            torpedo.move(self.__screen_min_x, self.__screen_max_x,
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

        for torpedo in self.__torpedoes:
            self.__screen.draw_torpedo(torpedo, torpedo.x, torpedo.y, torpedo.degrees)

        self.__screen.set_score(self.__score)

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
        self.__torpedoes_asteroid_hit()

        if self.__screen.is_left_pressed():
            self.__ship.change_heading(1)
        if self.__screen.is_right_pressed():
            self.__ship.change_heading(0)
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
        if self.__screen.is_space_pressed() and len(self.__torpedoes) < MAX_TORPEDO_NUM:
            x_speed = self.__ship.speed_x + 2 * math.cos(math.radians(self.__ship.heading))
            y_speed = self.__ship.speed_y + 2 * math.sin(math.radians(self.__ship.heading))
            torpedo = Torpedo(self.__ship.x, self.__ship.y, self.__ship.heading, x_speed, y_speed)
            self.__torpedoes.append(torpedo)
            self.__screen.register_torpedo(torpedo)
        self.__remove_old_torpedoes()

    def __torpedoes_asteroid_hit(self):
        """
        Checks if one of the torpedoes hit one of the asteroids and acts appropriately
        """
        for asteroid in self.__asteroids:
            for torpedo in self.__torpedoes:
                if asteroid.has_intersection(torpedo):
                    self.__torpedo_hit(asteroid, torpedo)
                    # No need to continue scanning the other torpedoes if the asteroid was hit
                    break

    def __torpedo_hit(self, asteroid, torpedo):
        """
        A hit occurred, remove the hit asteroid and the hitting torpedo, and split the asteroid if i is a big one
        """
        self.__score += SCORE_TABLE[asteroid.size]
        new_asteroid_size = asteroid.size - 1

        # Remove and unregister the torpedo and the asteroid
        self.__screen.unregister_asteroid(asteroid)
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedoes = [curr_torpedo for curr_torpedo in self.__torpedoes if
                            curr_torpedo is not torpedo]
        self.__asteroids = [curr_asteroid for curr_asteroid in self.__asteroids if
                            curr_asteroid is not asteroid]

        # Split the asteroid if it is not a small one
        if new_asteroid_size != 0:
            speed_x = (torpedo.speed_x + asteroid.speed_x) / (
                    (asteroid.speed_x ** 2 + asteroid.speed_y ** 2) ** 0.5)
            speed_y = (torpedo.speed_y + asteroid.speed_y) / (
                    (asteroid.speed_x ** 2 + asteroid.speed_y ** 2) ** 0.5)

            # Create two asteroids with opposite speeds
            first_new_asteroid = Asteroid(asteroid.x, asteroid.y, new_asteroid_size, speed_x, speed_y)
            second_new_asteroid = Asteroid(asteroid.x, asteroid.y, new_asteroid_size, speed_x * -1,
                                           speed_y * -1)

            # Add and register the new asteroids
            self.__asteroids.append(first_new_asteroid)
            self.__asteroids.append(second_new_asteroid)
            self.__screen.register_asteroid(first_new_asteroid, new_asteroid_size)
            self.__screen.register_asteroid(second_new_asteroid, new_asteroid_size)

    def __remove_old_torpedoes(self):
        """
        Increase the age of the existing torpedoes and remove the old ones.
        """
        new_torpedoes = []
        for torpedo in self.__torpedoes:
            torpedo.increase_life()
            if torpedo.life <= MAX_TORPEDO_LIFE:
                new_torpedoes.append(torpedo)
            else:
                self.__screen.unregister_torpedo(torpedo)
        self.__torpedoes = new_torpedoes


def main(amount):
    runner = GameRunner(amount)
    runner.build_game()
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
