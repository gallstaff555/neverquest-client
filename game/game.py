#!/usr/bin/env python3 

import pygame, pytmx, pyscroll
from typing import Any
from game.config.config import Config
from game.actors.my_player import MyPlayer
from game.actors.player_npc_tracker import PlayerNPCTracker
from game.entities.player_mouse_reticle import PlayerMouseReticle
from client.client import Client
from pygame.sprite import Group, Sprite
import os,sys

cfg = Config()

class Game():
    def __init__(self, name: str, player_class: str, race: str, color: str) -> None:

        self._client = Client()

        pygame.init()
        self._screen = pygame.display.set_mode((cfg.SCREEN_WIDTH * cfg.CAMERA_SCALE, cfg.SCREEN_HEIGHT * cfg.CAMERA_SCALE), pygame.RESIZABLE)
        self._surface = pygame.Surface((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)).convert()
        pygame.display.set_caption("Test MMO")

        #set up map and pyscroll
        self._map_file = self.resource_path("assets/forest_1.tmx")
        self._tmx_data = pytmx.load_pygame(self._map_file)
        self._map_data = pyscroll.data.TiledMapData(self._tmx_data)
        self._my_map_layer = pyscroll.BufferedRenderer(self._map_data, (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), clamp_camera=True)
        self._camera_group = pyscroll.PyscrollGroup(map_layer=self._my_map_layer, default_layer=cfg.DEFAULT_PLAYER_LAYER)

        #set up player and add to camera_group
        animation_path = f"../assets/{race}/{player_class}/color_{color}"
        self._player = MyPlayer(name, player_class, race, cfg.PLAYER_START, animation_path, cfg.DEFAULT_ANIMATIONS)
        self._camera_group.add(self._player)
        
        # Track other players and npcs
        self._player_npc_tracker = PlayerNPCTracker(self._player, self._camera_group)

        # set up invisible collision sprites
        self._collision_group: Group = pygame.sprite.Group()
        self._object_layer = self._tmx_data.get_layer_by_name("Collision")
        for obj in self._object_layer:
            sprite_image = pygame.Surface((5, 5))  
            sprite_image.fill(pygame.Color('blue')) 
            sprite_mask = pygame.mask.from_surface(sprite_image) 
            sprite: Sprite = pygame.sprite.Sprite() 
            sprite.image = sprite_image
            sprite.rect = sprite.image.get_rect(center = (obj.x, obj.y))
            #sprite.mask = sprite_mask
            self._collision_group.add(sprite)

        # set up projectiles and aim reticle
        self._projectiles_group: Group = pygame.sprite.Group()
        self._reticle = PlayerMouseReticle(self._surface)

        #pygame set up
        self.clock = pygame.time.Clock()
        self.scale = pygame.transform.scale
        self.running = True 



    def resource_path(self, relative_path: str) -> str:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def start_game(self) -> None:

        last_time = pygame.time.get_ticks()

        while self.running: 

            pygame.time.Clock().tick(cfg.FPS)

            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000.0  # Delta time in seconds
            last_time = current_time

            self._client.sync_server(self._player, cfg.GAME_SERVER_ENDPOINT, cfg.GAME_PORT)
            self._player_npc_tracker.update_other_players(self._client.get_other_player_location(), delta_time)
            # TODO add npc location update
            self._player_npc_tracker.update_npcs(self._client.get_npc_location(), delta_time)

            # Player should face the mouse pointer
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cam_x_offset, cam_y_offset = self._my_map_layer.view_rect.topleft
            true_mouse_x = mouse_x / cfg.CAMERA_SCALE
            true_mouse_y = mouse_y / cfg.CAMERA_SCALE
            if true_mouse_x + cam_x_offset < self._player.rect.center[0]:
                self._player.flipped = True 
            else:
                self._player.flipped = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self._client.disconnect_from_server(self._player.name, cfg.GAME_SERVER_ENDPOINT, cfg.GAME_PORT)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if cfg.MOVEMENT_TYPE == "mouse":
                        #calculate player true position with camera and camera scale offset 
                        world_x, world_y = true_mouse_x + cam_x_offset, true_mouse_y + cam_y_offset
                        self._player.move_to = (round(world_x), round(world_y))

            # update player positions and draw to screen 
            self._player.update_pos(self._collision_group, delta_time)
            self._camera_group.update(self._collision_group)
            self._camera_group.center(self._player.rect.center)
            self._camera_group.draw(self._surface)

            #pygame.draw.circle(self._surface, pygame.Color(255,255,255), (true_mouse_x, true_mouse_y), 2, 2)
            self._reticle.draw(true_mouse_x, true_mouse_y)

            self.scale(self._surface, self._screen.get_size(), self._screen)
            pygame.display.flip()


        self._client.disconnect_from_server(self._player.name, cfg.GAME_SERVER_ENDPOINT, cfg.GAME_PORT)
        pygame.quit()
        sys.exit()