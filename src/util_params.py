import os

# Screen Dimensions
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN_TERMINAL = (0, 255, 0)
DARK_GREY = (20, 20, 20)
LIGHT_GREY = (100, 100, 100)
BLUE_UI = (0, 120, 215)


# Game Settings
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_BASE_SPEED = 0.5
WAVE_BONUS_SPEED = 0.3

SCORE_PER_HIT = 50

# Files and Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets')
AUDIO_DIR = os.path.join(ASSETS_DIR, 'Audio')
PLAYERS_DIR = os.path.join(ASSETS_DIR, 'players')
BG_DIR = os.path.join(ASSETS_DIR, 'bg')
WEAPONS_DIR = os.path.join(ASSETS_DIR, 'weapons')
HIGH_SCORE_FILE = os.path.join(BASE_DIR, '..', 'high_scores.json')


# Audio Files
GAME_OVER_SOUND = os.path.join(AUDIO_DIR, 'impactBell_heavy_000.ogg')
