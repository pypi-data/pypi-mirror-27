from BrickBreaker.Bricks import Brick
from BrickBreaker.Shared import *


class SpeedBrick(Brick):

    def __init__(self, position, image, game):
        super().__init__(position, image, game)

    def hit(self):
        game = self.get_game()

        for ball in game.get_balls():
            ball.set_speed(ball.get_speed() + 1)

        super().hit()

    @staticmethod
    def get_hit_sound():
        return GameConstants.SOUND_HIT_SPEED_UP

