from pkg_resources import resource_filename


class GameConstants:

    SCREEN_SIZE = [1600, 900]
    BRICK_SIZE = [SCREEN_SIZE[0] / 16, SCREEN_SIZE[1] / 30]
    BALL_SIZE = [16, 16]
    PAD_SIZE = [139, 13]
    DOUBLE_PAD_SIZE = [278, 13]

    BALL_IMAGE = resource_filename(__name__, "ball.png")
    STANDARD_BRICK_IMAGE = resource_filename(__name__, "standard_brick_try.png")
    SPEED_BRICK_IMAGE = resource_filename(__name__, "speed_brick_try.png")
    LIFE_BRICK_IMAGE = resource_filename(__name__, "life_brick_try.png")
    BALL_BRICK_IMAGE = resource_filename(__name__, "extra_ball_try.png")
    SIZE_BRICK_IMAGE = resource_filename(__name__, "bonus_size_try.png")
    PAD_IMAGE = resource_filename(__name__, "pad.png")
    HIGHSCORE_IMAGE = resource_filename(__name__, "high_score.png")
    MAIN_MENU_IMAGE = resource_filename(__name__, "main_menu.png")
    DOUBLE_PAD_IMAGE = resource_filename(__name__, "double_pad.png")

    SOUND_FILE_HITTING_A_STANDARD_BRICK = resource_filename(__name__, "ball_hitting_a_wall_or_a_pad.wav")
    SOUND_FILE_HITTING_SPEED_UP_BRICK = resource_filename(__name__, "hitting_speed_up_brick.wav")
    SOUND_FILE_HITTING_EXTRA_LIFE_BRICK = resource_filename(__name__, "hitting_extra_life_brick.wav")
    SOUND_FILE_BALL_HITTING_A_WALL_OR_A_PAD = resource_filename(__name__, "ball_hitting_a_wall_or_a_pad.wav")
    SOUND_FILE_GAME_OVER = resource_filename(__name__, "game_over.wav")
    SOUND_FILE_HITTING_EXTRA_BALL_BRICK = resource_filename(__name__, "extra_ball.wav")
    SOUND_FILE_HITTING_BONUS_SIZE_BRICK = resource_filename(__name__, "bonus_size.wav")

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
