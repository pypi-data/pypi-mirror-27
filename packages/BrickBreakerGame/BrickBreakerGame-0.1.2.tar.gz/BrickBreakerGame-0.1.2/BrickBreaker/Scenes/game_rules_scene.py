import pygame

from BrickBreaker.Scenes.scene import Scene
from BrickBreaker.Shared import *


class GameRulesScene(Scene):

    def __init__(self, game):
        super().__init__(game)

    def render(self):

        self.clear_text()
        self.add_text("WELCOME TO BRICK BREAKER", x=450, y=50, size=60)
        self.add_text("Each brick is worth 100 points. After hitting speed brick speed of all active balls "
                      "will increase by set amount. You can stack 2 of these buffs per ball.", x=100, y=200, size=30)
        self.add_text("Hitting speed brick will also make all bricks be worth double of their initial value. "
                      "This applies to the extra(bonus) points as well and can be stacked ", x=100, y=250, size=30)
        self.add_text("indefinetly. Both bonus and speed buff will reset upon losing a life. Each life "
                      "brick you hit will increase total amount of your life by one. If you ", x=100, y=300, size=30)
        self.add_text("complete the game every extra life you have left will increase your final score "
                      "by 10 000. Bonus size bricks will double the size of your pad. ", x=100, y=350, size=30)
        self.add_text("These are not stackable. However they will grant you extra 1000 points upon hitting "
                      "them if you are already affected by the buff they provide. Extra ball ", x=100, y=400, size=30)
        self.add_text("bricks will give you an extra ball after you hit them and there is no limit to the amount "
                      "of balls you can have active at one time. If you have more than ", x=100, y=450, size=30)
        self.add_text("one ball active and you miss the ball with your pad that ball will be lost, "
                      "but you won't lose life. You start on level 1 with a single row of ", x=100, y=500, size=30)
        self.add_text("bricks, with each next level increasing the amount of rows, and thus "
                      "the difficulty. There is total of eight levels.", x=100, y=550, size=30)
        # self.add_text("the difficulty. There is total of eight levels.", x=100, y=550, size=30 )
        self.add_text("F1 - Back to Main Menu", x=300, y=800, size=60)

        super().render()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.get_game().change_scene(GameConstants.MAIN_MENU_SCENE)

                if event.key == pygame.K_F1:
                    self.get_game().change_scene(GameConstants.MAIN_MENU_SCENE)
