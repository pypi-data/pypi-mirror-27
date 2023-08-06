import os


class GameConstants:

    SCREEN_SIZE = [1600, 900]
    BRICK_SIZE = [SCREEN_SIZE[0] / 16, SCREEN_SIZE[1] / 30]
    BALL_SIZE = [16, 16]
    PAD_SIZE = [139, 13]
    DOUBLE_PAD_SIZE = [278, 13]

    BALL_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/ball.png"
    STANDARD_BRICK_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/standard_brick_try.png"
    SPEED_BRICK_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/speed_brick_try.png"
    LIFE_BRICK_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/life_brick_try.png"
    BALL_BRICK_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/extra_ball_try.png"
    SIZE_BRICK_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/bonus_size_try.png"
    PAD_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/pad.png"
    HIGHSCORE_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/high_score.png"
    MAIN_MENU_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/main_menu.png"
    DOUBLE_PAD_IMAGE = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/double_pad.png"

    SOUND_FILE_HITTING_A_STANDARD_BRICK = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/hitting_a_" \
                                          "standard_brick.wav"
    SOUND_FILE_HITTING_SPEED_UP_BRICK = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/hitting_speed_" \
                                        "up_brick.wav"
    SOUND_FILE_HITTING_EXTRA_LIFE_BRICK = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/hitting_extra_" \
                                          "life_brick.wav"
    SOUND_FILE_BALL_HITTING_A_WALL_OR_A_PAD = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/ball_hitting_" \
                                              "a_wall_or_a_pad.wav"
    SOUND_FILE_GAME_OVER = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/game_over.wav"
    SOUND_FILE_HITTING_EXTRA_BALL_BRICK = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/extra_ball.wav"
    SOUND_FILE_HITTING_BONUS_SIZE_BRICK = "/home/uros/Projects/BrickBreaker/BrickBreaker/Assets/bonus_size.wav"

    SOUND_HIT_BRICK = 0
    SOUND_HIT_SPEED_UP = 1
    SOUND_HIT_EXTRA_LIFE = 2
    SOUND_HIT_WALL_OR_PAD = 3
    SOUND_GAME_OVER = 4
    SOUND_HIT_EXTRA_BALL = 5
    SOUND_HIT_BONUS_SIZE = 6

    PLAYING_SCENE = 0
    HIGHSCORE_SCENE = 1
    MAIN_MENU_SCENE = 2
    GAME_OVER_SCENE = 3
    WIN_SCENE = 4
    CONTROLS_SCENE = 5
    GAME_RULES_SCENE = 6
