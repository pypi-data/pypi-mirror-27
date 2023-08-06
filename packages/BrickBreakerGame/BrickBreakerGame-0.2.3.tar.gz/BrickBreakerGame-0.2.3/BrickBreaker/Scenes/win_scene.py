import pygame

from BrickBreaker.Scenes.scene import Scene
from BrickBreaker.Shared import *
from BrickBreaker import Highscore


class WinScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self._player_name = ""

    def render(self):

        self._game.screen.fill((120, 0, 120))

        self.clear_text()
        self.add_text("YOU WIN!", x=600, y=200, size=100, color=[242, 111, 0], background=[120, 0, 120],
                      font_type="Ani", italic=True, bold=True)
        self.add_text("Q - Start New Game", x=300, y=500, background=[120, 0, 120], size=30)
        self.add_text("W - Quit", x=1100, y=500, background=[120, 0, 120], size=30)
        self.add_text("Please enter your name: ", x=700, y=700, background=[120, 0, 120], size=30)
        self.add_text(self._player_name, x=700, y=800, background=[120, 0, 120], size=30)

        super().render()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

                if event.key == pygame.K_q:
                    self.get_game().reset()
                    self.get_game().change_scene(GameConstants.PLAYING_SCENE)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game = self.get_game()
                        Highscore().add(self._player_name, game.get_score() + game.get_lives() * 10000)
                        game.reset()
                        game.change_scene(GameConstants.HIGHSCORE_SCENE)
                    elif 122 >= event.key >= 65:
                        self._player_name += chr(event.key)

                if event.key == pygame.K_w:
                    exit()
