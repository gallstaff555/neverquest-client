#!/usr/bin/env python3 

import pygame, pytmx, pyscroll
from game.config.config import Config
from game.actors.my_player import MyPlayer
from game.actors.player_tracker import PlayerTracker
from game.entities.player_mouse_reticle import PlayerMouseReticle
from client.client import Client
import os,sys

cfg = Config()

class Game():
    def __init__(self, name, player_class, race, color):

        self.client = Client()

        pygame.init()
        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH * cfg.CAMERA_SCALE, cfg.SCREEN_HEIGHT * cfg.CAMERA_SCALE), pygame.RESIZABLE)
        self.surface = pygame.Surface((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)).convert()
        pygame.display.set_caption("Test MMO")

        #set up map and pyscroll
        self.map_file = self.resource_path("assets/forest_1.tmx")
        self.tmx_data = pytmx.load_pygame(self.map_file)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.my_map_layer = pyscroll.BufferedRenderer(self.map_data, (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), clamp_camera=True)
        self.camera_group = pyscroll.PyscrollGroup(map_layer=self.my_map_layer, default_layer=cfg.DEFAULT_PLAYER_LAYER)

        #set up player and add to camera_group
        animation_path = f"../assets/{race}/{player_class}/color_{color}"
        self.player = MyPlayer(name, player_class, race, cfg.PLAYER_START, animation_path, cfg.DEFAULT_ANIMATIONS)
        self.camera_group.add(self.player)
        self.player_tracker = PlayerTracker(self.player, self.camera_group)

        # set up invisible collision sprites
        self.collision_group = pygame.sprite.Group()
        self.object_layer = self.tmx_data.get_layer_by_name("Collision")
        for obj in self.object_layer:
            sprite_image = pygame.Surface((5, 5))  
            sprite_image.fill(pygame.Color('blue')) 
            sprite_mask = pygame.mask.from_surface(sprite_image) 
            sprite = pygame.sprite.Sprite() 
            sprite.image = sprite_image
            sprite.rect = sprite.image.get_rect(center = (obj.x, obj.y))
            sprite.mask = sprite_mask
            self.collision_group.add(sprite)

        # set up projectiles and aim reticle
        self.projectiles_group = pygame.sprite.Group()
        self.reticle = PlayerMouseReticle(self.surface)

        #pygame set up
        self.clock = pygame.time.Clock()
        self.scale = pygame.transform.scale
        self.running = True 



    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def start_game(self):

        last_time = pygame.time.get_ticks()

        while self.running: 

            pygame.time.Clock().tick(cfg.FPS)

            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000.0  # Delta time in seconds
            last_time = current_time

            self.client.sync_server(self.player, cfg.GAME_SERVER_ENDPOINT, cfg.GAME_PORT)
            self.player_tracker.update_other_players(self.client.get_data_from_server(), delta_time)

            # Player should face the mouse pointer
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cam_x_offset, cam_y_offset = self.my_map_layer.view_rect.topleft
            true_mouse_x = mouse_x / cfg.CAMERA_SCALE;
            true_mouse_y = mouse_y / cfg.CAMERA_SCALE;
            if true_mouse_x + cam_x_offset < self.player.rect.center[0]:
                self.player.flipped = True 
            else:
                self.player.flipped = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.client.disconnect_from_server(self.player.name, cfg.GAME_SERVER_ENDPOINT, cfg.GAME_PORT)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if cfg.MOVEMENT_TYPE == "mouse":
                        #calculate player true position with camera and camera scale offset 
                        world_x, world_y = true_mouse_x + cam_x_offset, true_mouse_y + cam_y_offset
                        self.player.move_to = (round(world_x), round(world_y))

            # update player positions and draw to screen 
            self.player.update_pos(self.collision_group, delta_time)
            self.camera_group.update(self.collision_group)
            self.camera_group.center((self.player.rect.center))
            self.camera_group.draw(self.surface)

            #pygame.draw.circle(self.surface, pygame.Color(255,255,255), (true_mouse_x, true_mouse_y), 2, 2)
            self.reticle.draw(true_mouse_x, true_mouse_y)

            self.scale(self.surface, self.screen.get_size(), self.screen)
            pygame.display.flip()


        self.client.disconnect_from_server(self.player.name)
        pygame.quit()
        sys.exit()