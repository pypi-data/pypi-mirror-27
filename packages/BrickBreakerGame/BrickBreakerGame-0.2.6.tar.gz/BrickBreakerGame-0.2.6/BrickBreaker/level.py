import random

from BrickBreaker.Bricks import *
from BrickBreaker.Shared import *

import pygame


class Level:

    def __init__(self, game):
        self._game = game
        self._bricks = []
        self._amount_of_bricks_left = 0
        self._current_level = 1

    def get_bricks(self):
        return self._bricks

    def get_game(self):
        return self._game

    def get_amount_of_bricks_left(self):
        return self._amount_of_bricks_left

    def brick_hit(self):
        self._amount_of_bricks_left -= 1

    def load_next_level(self):
        self._current_level += 1
        self.load_random()

    def load_random(self):

        if self._current_level >= 9:
            self.get_game().change_scene(GameConstants.WIN_SCENE)

        self._bricks = []

        x, y = 0, 0

        max_bricks = int(GameConstants.SCREEN_SIZE[0] / GameConstants.BRICK_SIZE[0])
        rows = self._current_level + 1

        for row in range(0, rows):
            amount_of_life_bricks = 0
            amount_of_speed_bricks = 0
            amount_of_ball_bricks = 0
            amount_of_size_bricks = 0

            for brick in range(0, max_bricks):
                brick_type = random.randint(2, 5)

                if brick % 2 == 1:

                    if brick_type == 2 and amount_of_speed_bricks < self._current_level * 2:
                        brick = SpeedBrick([x, y], pygame.image.load(GameConstants.SPEED_BRICK_IMAGE), self._game)
                        self._bricks.append(brick)
                        self._amount_of_bricks_left += 1
                        amount_of_speed_bricks += 1

                    elif brick_type == 3 and amount_of_life_bricks < self._current_level * 2:
                        brick = LifeBrick([x, y], pygame.image.load(GameConstants.LIFE_BRICK_IMAGE), self._game)
                        self._bricks.append(brick)
                        self._amount_of_bricks_left += 1
                        amount_of_life_bricks += 1

                    elif brick_type == 4 and amount_of_size_bricks < self._current_level * 2:
                        brick = SizeBrick([x, y], pygame.image.load(GameConstants.SIZE_BRICK_IMAGE), self._game)
                        self._bricks.append(brick)
                        self._amount_of_bricks_left += 1
                        amount_of_size_bricks += 1

                    elif brick_type == 5 and amount_of_ball_bricks < self._current_level * 2:
                        brick = BallBrick([x, y], pygame.image.load(GameConstants.BALL_BRICK_IMAGE), self._game)
                        self._bricks.append(brick)
                        self._amount_of_bricks_left += 1
                        amount_of_ball_bricks += 1
                    else:
                        brick = Brick([x, y], pygame.image.load(GameConstants.STANDARD_BRICK_IMAGE), self._game)
                        self._bricks.append(brick)
                        self._amount_of_bricks_left += 1

                else:
                    brick = Brick([x, y], pygame.image.load(GameConstants.STANDARD_BRICK_IMAGE), self._game)
                    self._bricks.append(brick)
                    self._amount_of_bricks_left += 1

                x += GameConstants.BRICK_SIZE[0]

            x = 0
            y += GameConstants.BRICK_SIZE[1]

