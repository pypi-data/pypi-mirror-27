from BrickBreaker.Shared import GameObject
from BrickBreaker.Shared import GameConstants


class Brick(GameObject):

    def __init__(self, position, image, game):
        self._game = game
        self._hit_points = 100
        self._lives = 1

        super().__init__(position, GameConstants.BRICK_SIZE, image)

    def get_game(self):
        return self._game

    def is_destroyed(self):
        return self._lives < 1

    def get_hit_points(self):
        return self._hit_points

    def hit(self):
        self._lives -= 1

    @staticmethod
    def get_hit_sound():
        return GameConstants.SOUND_HIT_BRICK
