import pygame

class Config:

    # General
    TEST = True
    SCALE = 1
    CAMERA_SCALE = 2
    TILE_SIZE = 16
    COL = 20
    ROW = 20
    SCREEN_WIDTH = TILE_SIZE * COL * SCALE
    SCREEN_HEIGHT = TILE_SIZE * ROW * SCALE 
    DEFAULT_LEVEL_SIZE = SCREEN_WIDTH
    FPS = 30
    
    # Player
    PLAYER_START = (170, 120)
    PLAYER_ANIMATION_TIMER = 100
    PLAYER_SPRITE_SIZE = 64
    DEFAULT_PLAYER_LAYER = 2
    SPEED = 3
    DIAG_SPEED = SPEED * .7071

    # ANIMATION
    #DEFAULT_ANIMATIONS_LIST = ["walk", "idle"]
    #DEFAULT_ANIMATIONS = {"idle": 6, "walk": 6, "attack": 6, "death": 6} # action: frames
    DEFAULT_ANIMATIONS = {"idle": 6, "walk": 6, "attack": 6}
    
    # ELF ANIMATION
    RACE = "ELF"
    DEFAULT_ELF_ANIMATION_PATH = "../assets/elf/archer/color_3"
    #ELF = {"path": DEFAULT_ELF_ANIMATION_PATH, "frames": DEFAULT_ELF_ANIMATIONS, "race": RACE}

    # CONTROLS
    MOVEMENT_TYPE = "keyboard"
    key_left = pygame.K_LEFT
    key_right = pygame.K_RIGHT
    key_down = pygame.K_DOWN
    key_up = pygame.K_UP