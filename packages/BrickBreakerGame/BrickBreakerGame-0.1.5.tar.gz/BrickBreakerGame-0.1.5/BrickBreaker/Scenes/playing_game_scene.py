import pygame

from BrickBreaker.Scenes.scene import Scene
from BrickBreaker.Shared import *


class PlayingGameScene(Scene):

    def __init__(self, game):
        super().__init__(game)

    def render(self):
        super().render()

        game = self.get_game()
        level = game.get_level()
        pad = game.get_pad()
        balls = game.get_balls()

        if level.get_amount_of_bricks_left() <= 0:
            for ball in balls:
                ball.set_motion(0)
                ball.update_position()

            level.load_next_level()

        if game.get_lives() <= 0:
            game.play_sound(GameConstants.SOUND_GAME_OVER)
            game.change_scene(GameConstants.GAME_OVER_SCENE)

        for ball in balls:
            for ball2 in balls:
                if ball != ball2 and ball.intersects(ball2):
                    ball.change_direction(ball2)

            for brick in game.get_level().get_bricks():
                if not brick.is_destroyed() and ball.intersects(brick):
                    game.play_sound(brick.get_hit_sound())
                    brick.hit()
                    level.brick_hit()
                    if brick.get_hit_sound() == 1:
                        game.increment_bonus()
                    game.increase_score(brick.get_hit_points())
                    ball.change_direction(brick)
                    break

            if ball.intersects(pad):
                game.play_sound(GameConstants.SOUND_HIT_WALL_OR_PAD)
                ball.change_direction(pad)

            ball.update_position()

            if ball.is_ball_dead():
                if len(balls) <= 1:
                    ball.set_motion(0)
                    game.reduce_life_by_one()
                    game.reset_bonus()
                    game.reset_pad()
                else:
                    balls.remove(ball)

            game.screen.blit(ball.get_image(), ball.get_position())

        for brick in game.get_level().get_bricks():
            if not brick.is_destroyed():
                game.screen.blit(brick.get_image(), brick.get_position())

        if pad.get_keyboard_status():

            pad.set_position((pad.get_position()[0], pad.get_position()[1]))
            if pad.right_is_pressed:
                pad.set_position((pad.get_position()[0] + 15, pad.get_position()[1]))
            if pad.left_is_pressed:
                pad.set_position((pad.get_position()[0] - 15, pad.get_position()[1]))

        if pad.get_mouse_status():
            pad.set_position((pygame.mouse.get_pos()[0], pad.get_position()[1]))

        game.screen.blit(pad.get_image(), pad.get_position())

        self.clear_text()

        self.add_text("Your score: " + str(game.get_score()), x=0, y=GameConstants.SCREEN_SIZE[1] - 60, size=30)

        self.add_text("Lives: " + str(game.get_lives()), x=0, y=GameConstants.SCREEN_SIZE[1] - 30, size=30)

        self.add_text(f"Bonus: x{str(game.get_bonus())}", x=GameConstants.SCREEN_SIZE[0] - 100,
                      y=GameConstants.SCREEN_SIZE[1] - 30, size=30)

    def handle_events(self, events):
        super().handle_events(events)
        game = self.get_game()
        pad = game.get_pad()

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for ball in self.get_game().get_balls():
                    ball.set_motion(1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for ball in self.get_game().get_balls():
                        ball.set_motion(1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pad.left_pressed(True)
                if event.key == pygame.K_RIGHT:
                    pad.right_pressed(True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pad.left_pressed(False)
                if event.key == pygame.K_RIGHT:
                    pad.right_pressed(False)
