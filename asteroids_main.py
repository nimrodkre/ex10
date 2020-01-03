import math

from screen import Screen
import sys
from random import randint
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo

SCORE_TABLE = {
    3: 20,
    2: 50,
    1: 100
}
DEFAULT_ASTEROIDS_NUM = 5
ASTEROID_SIZE = 3
ASTEROID_MIN_SPEED_X = 1
ASTEROID_MAX_SPEED_X = 4
ASTEROID_MIN_SPEED_Y = 1
ASTEROID_MAX_SPEED_Y = 4
MAX_TORPEDO_NUM = 10
MAX_TORPEDO_LIFE = 200
START_SCORE = 0
START_LIFE = 3
SHIP_HEADER_START = 0
SHIP_SPEED_X_START = 0
SHIP_SPEED_Y_START = 0


class GameRunner:
    """
    Manages an Asteroids game
    """
    def __init__(self, asteroids_amount):
        """
        Creates a new asteroids game
        :param asteroids_amount: The initial amount of asteroids in the game
        """
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroids_amount = asteroids_amount

        self.__ship = None
        self.__asteroids = None
        self.__torpedoes = []
        self.__score = START_SCORE
        self.__life = START_LIFE

        self.__build_game()

    def __build_game(self):
        """
        in charge of building the game, ships and asteroids at the beginning
        :return: None
        """
        self.__ship = Ship(randint(self.__screen_min_x, self.__screen_max_x),
                           randint(self.__screen_min_y, self.__screen_max_y),
                           SHIP_HEADER_START, SHIP_SPEED_X_START,
                           SHIP_SPEED_Y_START)

        self.__asteroids = self.__build_asteroids(self.__asteroids_amount)

        for asteroid in self.__asteroids:
            self.__screen.register_asteroid(asteroid, asteroid.size)

    def __build_asteroids(self, asteroids_amounts):
        """
        builds the asteroids
        :param asteroids_amounts: number of asteroids to build 
        :return: list with all asteroids
        """
        asteroids = []

        for i in range(asteroids_amounts):
            asteroid = Asteroid(randint(self.__screen_min_x,
                                        self.__screen_max_x),
                                randint(self.__screen_min_y,
                                        self.__screen_max_y),
                                ASTEROID_SIZE, randint(ASTEROID_MIN_SPEED_X,
                                                       ASTEROID_MAX_SPEED_X),
                                randint(ASTEROID_MIN_SPEED_Y,
                                        ASTEROID_MAX_SPEED_Y))
            while asteroid.has_intersection(self.__ship):
                asteroid = Asteroid(randint(self.__screen_min_x,
                                            self.__screen_max_x),
                                    randint(self.__screen_min_y,
                                            self.__screen_max_y),
                                    ASTEROID_SIZE,
                                    randint(ASTEROID_MIN_SPEED_X,
                                            ASTEROID_MAX_SPEED_X),
                                    randint(ASTEROID_MIN_SPEED_Y,
                                            ASTEROID_MAX_SPEED_Y))
            asteroids.append(asteroid)

        return asteroids

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again

        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def __move_all_gamepieces(self):
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

    def __draw_all_gamepieces(self):
        """
        draws all gamepieces, ships, asteroids, torpedoes
        :return: None
        """
        self.__screen.draw_ship(self.__ship.x, self.__ship.y,
                                self.__ship.heading)

        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.x, asteroid.y)

        for torpedo in self.__torpedoes:
            self.__screen.draw_torpedo(torpedo, torpedo.x, torpedo.y,
                                       torpedo.degrees)

        self.__screen.set_score(self.__score)

    def __ship_asteroid_collision(self):
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
                self.__life -= 1
                collided_asteroids.append(asteroid)

        self.__remove_asteroids(collided_asteroids)

    def __remove_asteroids(self, asteroids):
        """
        removes the given asteroids from the game board
        :param asteroids: The asteroids to remove
        :return: None
        """
        for asteroid in asteroids:
            self.__screen.unregister_asteroid(asteroid)
            self.__asteroids.remove(asteroid)

    def __remove_torpedoes(self, torpedoes):
        """
        removes the given torpedoes from the game board
        :param torpedoes: The asteroids to remove
        :return: None
        """
        for torpedo in torpedoes:
            self.__screen.unregister_torpedo(torpedo)
            self.__torpedoes.remove(torpedo)

    def _game_loop(self):
        """
        The brain of the game, in charge of moving pieces and checking if 
        a command has been evoked.
        :return: 
        """
        game_over_msg = self.__is_game_over()
        if game_over_msg is not None:
            self.__screen.show_message("Game Over", game_over_msg)
            self.__screen.end_game()
            sys.exit()

        self.__draw_all_gamepieces()
        self.__move_all_gamepieces()

        self.__ship_asteroid_collision()
        self.__torpedoes_asteroid_hit()

        if self.__screen.is_left_pressed():
            self.__ship.change_heading(1)
        if self.__screen.is_right_pressed():
            self.__ship.change_heading(0)
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
        if self.__screen.is_space_pressed() and len(
                self.__torpedoes) < MAX_TORPEDO_NUM:
            self.__shoot_torpedo()

        self.__remove_old_torpedoes()


    def __shoot_torpedo(self):
        """
        Creates a new torpedo and adds it to the game
        :return: None
        """
        # Torpedo creation
        x_speed = self.__ship.speed_x + 2 * math.cos(
            math.radians(self.__ship.heading))
        y_speed = self.__ship.speed_y + 2 * math.sin(
            math.radians(self.__ship.heading))
        torpedo = Torpedo(self.__ship.x, self.__ship.y,
                          self.__ship.heading, x_speed, y_speed)

        # Adds and registers the new torpedo
        self.__torpedoes.append(torpedo)
        self.__screen.register_torpedo(torpedo)

    def __torpedoes_asteroid_hit(self):
        """
        Checks if one of the torpedoes hit one of the asteroids and acts
        appropriately
        :return: None
        """
        for asteroid in self.__asteroids:
            for torpedo in self.__torpedoes:
                if asteroid.has_intersection(torpedo):
                    self.__torpedo_hit(asteroid, torpedo)
                    # No need to continue scanning the other torpedoes if 
                    # the asteroid was hit once, so break inner loop
                    break

    def __torpedo_hit(self, asteroid, torpedo):
        """
        A hit occurred, remove the hit asteroid and the hitting torpedo, and 
        split the asteroid if i is a big one
        :return: None
        """
        self.__score += SCORE_TABLE[asteroid.size]

        # Remove and unregister the torpedo and the asteroid
        self.__remove_asteroids([asteroid])
        self.__remove_torpedoes([torpedo])

        # Split the asteroid if it is not a small one
        if asteroid.size != 1:
            self.__split_asteroid(asteroid, torpedo)

    def __split_asteroid(self, asteroid, torpedo):
        """
        Splits a hit asteroid
        :param asteroid: The asteroid that was hit
        :param torpedo: The hitting torpedo
        :return: None
        """
        new_asteroid_size = asteroid.size - 1
        speed_x = (torpedo.speed_x + asteroid.speed_x) / (
                (asteroid.speed_x ** 2 + asteroid.speed_y ** 2) ** 0.5)
        speed_y = (torpedo.speed_y + asteroid.speed_y) / (
                (asteroid.speed_x ** 2 + asteroid.speed_y ** 2) ** 0.5)
        # Create two asteroids with opposite speeds
        first_new_asteroid = Asteroid(asteroid.x, asteroid.y,
                                      new_asteroid_size, speed_x, speed_y)
        second_new_asteroid = Asteroid(asteroid.x, asteroid.y,
                                       new_asteroid_size, speed_x * -1,
                                       speed_y * -1)
        # Add and register the new asteroids
        self.__asteroids.append(first_new_asteroid)
        self.__asteroids.append(second_new_asteroid)
        self.__screen.register_asteroid(first_new_asteroid,
                                        new_asteroid_size)
        self.__screen.register_asteroid(second_new_asteroid,
                                        new_asteroid_size)

    def __remove_old_torpedoes(self):
        """
        Increase the age of the existing torpedoes and remove the old ones.
        :return: None
        """
        old_torpedoes = []
        for torpedo in self.__torpedoes:
            torpedo.increase_life()
            if torpedo.life > MAX_TORPEDO_LIFE:
                old_torpedoes.append(torpedo)
        self.__remove_torpedoes(old_torpedoes)

    def __is_game_over(self):
        """
        Checks if the game is over and creates an appropriate exit message
        :return: An exit message if the game is over, otherwise None
        """
        if self.__screen.should_end():
            return 'Sorry to see you want to leave. Good bye!'
        if self.__life == 0:
            return 'You fought bravely, but lost. Good bye!'
        if not any(self.__asteroids):
            return 'You saved the galaxy! No asteroids left!'
        return None


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
