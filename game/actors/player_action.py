import pygame,math
from game.config.config import Config

cfg = Config()

class PlayerAction():

    def move_by_coordinates(self, player, collision_group):
        dx = player.move_to[0] - player.pos[0]
        dy = player.move_to[1] - player.pos[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance > player.speed:
            if self.check_collision(player, collision_group):
                print("Collision!")
            temp_x = player.pos[0] + dx / distance * player.speed
            temp_y = player.pos[1] + dy / distance * player.speed
            player.pos = (temp_x, temp_y)
            player.rect.center = (temp_x, temp_y)
        else:
            if self.check_collision(player, collision_group):
                print("Collision!")
            temp_x = player.move_to[0]
            temp_y = player.move_to[1]
            player.pos = (temp_x, temp_y)
            player.rect.center = (temp_x, temp_y)
            return True
        return False
    
    def check_collision(self, player, collision_group):
        collisions = pygame.sprite.spritecollide(player, collision_group, False, pygame.sprite.collide_mask)
        for collided_sprite in collisions:
            return True
        
    def player_moving_action(self, player, keys, animator, action):
        if keys[cfg.key_up] and player.rect.y > -20:
            player.direction_y = -1
            if player.flipped:
                animator.player_frames = animator.animation_map[f"{action}_flipped"]
            else:
                animator.player_frames = animator.animation_map[f"{action}"]
            
            if keys[cfg.key_down] or keys[cfg.key_left]:
                player.speed = cfg.DIAG_SPEED
            else:
                player.speed = cfg.SPEED
        elif keys[cfg.key_down] and player.rect.y < cfg.DEFAULT_LEVEL_SIZE * 1.5 - 55:
            player.direction_y = 1
            if player.flipped:
                animator.player_frames = animator.animation_map[f"{action}_flipped"]
            else:
                animator.player_frames = animator.animation_map[f"{action}"]

            if keys[cfg.key_right] or keys[cfg.key_right]:
                player.speed = cfg.DIAG_SPEED
            else:
                player.speed = cfg.SPEED
        else:
            player.direction_y = 0

        if keys[cfg.key_right] and player.rect.x < cfg.DEFAULT_LEVEL_SIZE * 1.5 - 40:
            player.direction_x = 1
            animator.player_frames = animator.animation_map[f"{action}"]
            player.flipped = False
        elif keys[cfg.key_left] and player.rect.x > -20:
            player.direction_x = -1
            player.flipped = True
            animator.player_frames = animator.animation_map[f"{action}_flipped"]
        else:
            player.direction_x = 0  

    def player_idle_action(self, player, animator, action):
        #if not (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        player.moving = False
        if player.flipped:
            animator.player_frames = animator.animation_map[f"{action}_flipped"]
        else:
            animator.player_frames = animator.animation_map[f"{action}"]


    def keyboard_input(self, player, animator):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or player.attacking:
            if not player.attacking: #reset attack animation
                animator.index = 0
            player.attacking = True

        if not (keys[cfg.key_down] or keys[cfg.key_left] or keys[cfg.key_right] or keys[cfg.key_up]):
            player.moving = False
            player.direction_x = 0
            player.direction_y = 0
            if player.attacking:
                self.player_idle_action(player, animator, "attack")
            else:
                self.player_idle_action(player, animator, "idle")
        else:
            player.moving = True
            if player.attacking:
                self.player_moving_action(player, keys, animator, "attack")
            else:
                self.player_moving_action(player, keys, animator, "walk")
            

    def update(self, player, animator, collision_group):
        if cfg.MOVEMENT_TYPE == "keyboard":
            self.keyboard_input(player, animator)
            player.rect.x += player.direction_x * player.speed
            player.rect.y += player.direction_y * player.speed 
            if self.check_collision(player, collision_group):
                player.rect.x -= player.direction_x * player.speed
                player.rect.y -= player.direction_y * player.speed

        elif cfg.MOVEMENT_TYPE == "mouse" and player.move_to:
            if self.move_by_coordinates(player, collision_group):
                player.move_to = None  