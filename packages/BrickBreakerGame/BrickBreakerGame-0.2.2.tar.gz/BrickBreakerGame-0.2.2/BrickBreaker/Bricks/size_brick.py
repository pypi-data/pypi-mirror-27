from BrickBreaker.Bricks import Brick
from BrickBreaker.Shared import *
from BrickBreaker.pad import Pad


class SizeBrick(Brick):

    def __init__(self, position, image, game):
        super().__init__(position, image, game)

    def hit(self):
        game = self.get_game()
        if isinstance(game.get_pad(), Pad):
            game.double_pad()
        else:
            game.increase_score_by_1k()

        super().hit()

    @staticmethod
    def get_hit_sound():
        return GameConstants.SOUND_HIT_BONUS_SIZE
