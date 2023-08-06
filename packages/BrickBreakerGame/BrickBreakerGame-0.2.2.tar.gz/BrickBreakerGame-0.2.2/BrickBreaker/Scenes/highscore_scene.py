import pygame

from BrickBreaker.Scenes.scene import Scene
from BrickBreaker import Highscore
from BrickBreaker.Shared import *


class HighscoreScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self._high_score_image = pygame.image.load(GameConstants.HIGHSCORE_IMAGE)

    def render(self):

        self.get_game().screen.blit(self._high_score_image, (15, 20))

        self.clear_text()

        highscore = Highscore()

        x = 600
        y = 100
        for position, score in enumerate(highscore.get_scores()):
            self.add_text(f"{position+1}. {score[0]}", x, y, size=45)
            self.add_text(str(score[1]), x + 200, y, size=45)

            y += 30

        self.add_text("F1 - Start Game", x, y + 120, size=60)
        self.add_text("F2 - Main Menu", x, y + 240, size=60)

        super().render()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.get_game().reset()
                    self.get_game().change_scene(GameConstants.PLAYING_SCENE)

                if event.key == pygame.K_F2:
                    self.get_game().change_scene(GameConstants.MAIN_MENU_SCENE)

                if event.key == pygame.K_ESCAPE:
                    self.get_game().change_scene(GameConstants.MAIN_MENU_SCENE)
