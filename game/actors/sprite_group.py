import pygame

class SpriteGroup(pygame.sprite.Group):
    def by_y(self, sprite):
        return sprite.pos.y
    
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for sprite in sorted(sprites, key=self.by_y):
            self.spritedict[sprite] = surface_blit(sprite.image, sprite.rect)
        self.lostsprites = []