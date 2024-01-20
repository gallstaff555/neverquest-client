import pygame
from game.config.config import Config
from game.actors.animate_player import AnimatePlayer

cfg = Config()

class BasePlayer(pygame.sprite.Sprite):
    def __init__(self, name, player_class, race, start_pos, animation_path, animation_frames):
        super().__init__()
        self.name = name
        self.player_class = player_class
        self.race = race
        self.animate_player = AnimatePlayer(animation_path, animation_frames)
        self.image = self.animate_player.player_frames[0]
        self.mask = self.animate_player.player_mask[0]
        self.rect = self.image.get_rect(center = start_pos)
        self.pos = start_pos
        self.move_to = None
        self.moving = False
        self.attacking = False
        self.speed = cfg.SPEED
        self.flipped = False
        self.direction_x = 0
        self.direction_y = 0
