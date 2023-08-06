from BrickBreaker.Shared import *
from BrickBreaker.pad import Pad


class Ball(GameObject):

    def __init__(self, position, image, game):
        self._game = game
        self._speed = 4
        self._speed_bonus = 1
        self._increment = [2, 2]
        self._direction = [1, 1]
        self._in_motion = 0

        super().__init__(position, GameConstants.BALL_SIZE, image)

    def set_speed(self, new_speed):
        if new_speed > 6:
            new_speed = 6
        self._speed = new_speed
        self._speed_bonus += 1

    def reset_speed(self):
        self.set_speed(4)

    def get_speed(self):
        return self._speed

    def is_in_motion(self):
        return self._in_motion

    def set_motion(self, is_moving):
        self._in_motion = is_moving
        self.reset_speed()

    def change_direction(self, game_object):

        position = self.get_position()
        size = self.get_size()
        object_position = game_object.get_position()
        object_size = game_object.get_size()

        if object_position[1] + object_size[1] > position[1] > object_position[1] and \
                object_position[0] + object_size[0] > position[0] > object_position[0]:
            self.set_position((position[0], object_position[1] + object_size[1]))
            self._direction[1] *= -1

        elif object_position[1] + object_size[1] > position[1] + size[1] > object_position[1] and \
                object_position[0] + object_size[0] > position[0] > object_position[0]:
            self.set_position((position[0], object_position[1] - object_size[1]))
            self._direction[1] *= -1

        elif object_position[0] + object_size[0] > position[0] + size[0] > object_position[0]:
            self.set_position((object_position[0] - size[0], position[1]))
            self._direction[0] *= -1

        else:
            self.set_position((object_position[0] + object_size[0], position[1]))
            self._direction[0] *= -1
            self._direction[1] *= -1

    def update_position(self):
        if not self.is_in_motion():
            pad_position = self._game.get_pad().get_position()
            if isinstance(self._game.get_pad(), Pad):
                self.set_position((
                    pad_position[0] + (GameConstants.PAD_SIZE[0] / 2) - (GameConstants.BALL_SIZE[0] / 2),
                    GameConstants.SCREEN_SIZE[1] - GameConstants.PAD_SIZE[1] - GameConstants.BALL_SIZE[1]
                ))
            else:
                self.set_position((
                    pad_position[0] + (GameConstants.DOUBLE_PAD_SIZE[0] / 2) - (GameConstants.BALL_SIZE[0] / 2),
                    GameConstants.SCREEN_SIZE[1] - GameConstants.DOUBLE_PAD_SIZE[1] - GameConstants.BALL_SIZE[1]
                ))
            return

        position = self.get_position()
        size = self.get_size()

        new_position = [position[0] + (self._increment[0] * self._speed) * self._direction[0],
                        position[1] + (self._increment[1] * self._speed) * self._direction[1]]

        if new_position[0] + size[0] >= GameConstants.SCREEN_SIZE[0]:
            self._direction[0] *= -1
            new_position = [GameConstants.SCREEN_SIZE[0] - size[0], new_position[1]]
            self._game.play_sound(GameConstants.SOUND_HIT_WALL_OR_PAD)

        if new_position[0] <= 0:
            self._direction[0] *= -1
            new_position = [0, new_position[1]]
            self._game.play_sound(GameConstants.SOUND_HIT_WALL_OR_PAD)

        if new_position[1] + size[1] >= GameConstants.SCREEN_SIZE[1]:
            self._direction[1] *= -1
            new_position = [new_position[0], GameConstants.SCREEN_SIZE[1] - size[1]]

        if new_position[1] <= 0:
            self._direction[1] *= -1
            new_position = [new_position[0], 0]
            self._game.play_sound(GameConstants.SOUND_HIT_WALL_OR_PAD)

        self.set_position(new_position)

    def is_ball_dead(self):
        position = self.get_position()
        size = self.get_size()

        if position[1] + size[1] >= GameConstants.SCREEN_SIZE[1]:
            return 1
        return 0
