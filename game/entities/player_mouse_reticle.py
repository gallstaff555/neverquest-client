import pygame

class PlayerMouseReticle():

    def __init__(self, surface):
        self.surface = surface

    def draw(self, mouse_x, mouse_y):
        pygame.draw.circle(self.surface, pygame.Color(255,255,255), (mouse_x, mouse_y), 2, 2)