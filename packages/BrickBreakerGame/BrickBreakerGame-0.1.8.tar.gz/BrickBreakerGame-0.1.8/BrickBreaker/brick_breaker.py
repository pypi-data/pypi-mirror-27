import pygame

from BrickBreaker import *
from BrickBreaker.Scenes import *
from BrickBreaker.Shared import *


class BrickBreaker:

    def __init__(self):
        self._lives = 5
        self._score = 0
        self._bonus = 1

        self._level = Level(self)
        self._level.load_random()

        self._pad = Pad((GameConstants.SCREEN_SIZE[0] / 2,
                        GameConstants.SCREEN_SIZE[1] - GameConstants.PAD_SIZE[1]),
                        pygame.image.load(GameConstants.PAD_IMAGE))

        self._balls = [
            Ball((400, 400), pygame.image.load(GameConstants.BALL_IMAGE), self)
        ]

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption("Brick Breaker")

        self._clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(GameConstants.SCREEN_SIZE)

        pygame.mouse.set_visible(False)

        self._scenes = (
            PlayingGameScene(self),
            MainMenuScene(self),
            GameOverScene(self),
            WinScene(self),
            ControlsScene(self),
            GameRulesScene(self),
        )

        self._current_scene = 1

        self._sounds = (
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HITTING_A_STANDARD_BRICK),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HITTING_SPEED_UP_BRICK),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HITTING_EXTRA_LIFE_BRICK),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_BALL_HITTING_A_WALL_OR_A_PAD),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_GAME_OVER),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HITTING_EXTRA_BALL_BRICK),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HITTING_BONUS_SIZE_BRICK),
        )

    def start(self):
        while True:
            self._clock.tick(60)

            self.screen.fill((0, 0, 0))

            _current_scene = self._scenes[self._current_scene]
            _current_scene.handle_events(pygame.event.get())
            _current_scene.render()

            pygame.display.update()

    def change_scene(self, scene):
        self._current_scene = scene

    def get_level(self):
        return self._level

    def get_bonus(self):
        return self._bonus

    def increment_bonus(self):
        self._bonus += 1

    def reset_bonus(self):
        self._bonus = 1

    def double_pad(self):
        keyboard = self._pad.get_keyboard_status()
        mouse = self._pad.get_mouse_status()
        self._pad = DoublePad((GameConstants.SCREEN_SIZE[0] / 2,
                              GameConstants.SCREEN_SIZE[1] - GameConstants.DOUBLE_PAD_SIZE[1]),
                              pygame.image.load(GameConstants.DOUBLE_PAD_IMAGE))
        if keyboard:
            self._pad.activate_keyboard()
        if mouse:
            self._pad.activate_mouse()

    def reset_pad(self):
        keyboard = self._pad.get_keyboard_status()
        mouse = self._pad.get_mouse_status()
        self._pad = Pad((GameConstants.SCREEN_SIZE[0] / 2,
                         GameConstants.SCREEN_SIZE[1] - GameConstants.PAD_SIZE[1]),
                        pygame.image.load(GameConstants.PAD_IMAGE))
        if keyboard:
            self._pad.activate_keyboard()
        if mouse:
            self._pad.activate_mouse()

    def get_pad(self):
        return self._pad

    def get_score(self):
        return self._score

    def increase_score(self, score):
        self._score += score * self._bonus

    def increase_score_by_1k(self, score=1000):
        self._score += score * self._bonus

    def get_lives(self):
        return self._lives

    def get_balls(self):
        return self._balls

    def add_one_ball(self):
        self._balls.append(Ball((400, 400), pygame.image.load(GameConstants.BALL_IMAGE), self))

    def play_sound(self, sound_clip):
        sound = self._sounds[sound_clip]

        sound.stop()
        sound.play()

    def reduce_life_by_one(self):
        self._lives -= 1

    def add_one_life(self):
        self._lives += 1

    def reset(self):
        self._lives = 5
        self._score = 0
        self._bonus = 1
        self._level = Level(self)
        self._level.load_random()

        self._pad = Pad((GameConstants.SCREEN_SIZE[0] / 2,
                         GameConstants.SCREEN_SIZE[1] - GameConstants.PAD_SIZE[1]),
                        pygame.image.load(GameConstants.PAD_IMAGE))


def main():
    BrickBreaker().start()


if __name__ == '__main__':
    BrickBreaker().start()
