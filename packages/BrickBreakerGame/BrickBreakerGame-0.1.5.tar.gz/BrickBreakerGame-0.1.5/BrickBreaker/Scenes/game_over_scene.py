import pygame

from BrickBreaker.Scenes.scene import Scene
from BrickBreaker.Shared import *


class GameOverScene(Scene):

    def __init__(self, game):
        super().__init__(game)

    def render(self):

        self._game.screen.fill((254, 60, 60))

        self.clear_text()
        self.add_text("GAME OVER!", x=400, y=200, size=100, color=[60, 60, 254], background=[254, 60, 60],
                      font_type="Ani", italic=True, bold=True)
        self.add_text("F1 - Start New Game", x=300, y=500, background=[254, 60, 60], size=30)
        self.add_text("F2 - Quit", x=1100, y=500, background=[254, 60, 60], size=30)

        super().render()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

                if event.key == pygame.K_F1:
                    self.get_game().reset()
                    self.get_game().change_scene(GameConstants.PLAYING_SCENE)

                if event.key == pygame.K_F2:
                    exit()
