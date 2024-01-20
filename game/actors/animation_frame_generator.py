import pygame 
import os,sys


class AnimationFrameGenerator():

    def get_frames(self, path, anim_dict, type, orientation):
        frames = []
        for i in range(0, anim_dict[type]):
            frame_file = self.resource_path(f"{path}/{type}/{orientation}/{type}_{i}.png")
            frame = pygame.image.load(frame_file).convert_alpha()
            frames.append(frame)
        masks = [pygame.mask.from_surface(frame) for frame in frames]
        return frames, masks
    
    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
