import pygame

from BrickBreaker.Scenes.scene import Scene
from BrickBreaker.Shared import *


class MainMenuScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self._menu_image = pygame.image.load(GameConstants.MAIN_MENU_IMAGE)

    def render(self):
        self.get_game().screen.blit(self._menu_image, (50, 50))

        self.clear_text()
        self.add_text("Q - Start Game", x=600, y=280, size=60)
        self.add_text("W - Highscore", x=600, y=360, size=60)
        self.add_text("E - Controls", x=600, y=440, size=60)
        self.add_text("R - Game Rules", x=600, y=520, size=60)
        self.add_text("T - Quit", x=600, y=600, size=60)

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
                    self.get_game().change_scene(GameConstants.PLAYING_SCENE)

                if event.key == pygame.K_w:
                    self.get_game().change_scene(GameConstants.HIGHSCORE_SCENE)

                if event.key == pygame.K_e:
                    self.get_game().change_scene(GameConstants.CONTROLS_SCENE)

                if event.key == pygame.K_r:
                    self.get_game().change_scene(GameConstants.GAME_RULES_SCENE)

                if event.key == pygame.K_t:
                    exit()

