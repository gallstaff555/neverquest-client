from game.actors.base_player import BasePlayer

class OtherPlayer(BasePlayer):
    def __init__(self, name, player_class, race, start_pos, animation_path, animation_frames):
        super().__init__(name, player_class, race, start_pos, animation_path, animation_frames)
        self.end_pos = start_pos
        self.interpolation_factor = 0.0

    def old_update_pos(self, new_coords, flipped, moving, attacking):
        #print(last_update)
        self.rect.x = new_coords[0]
        self.rect.y = new_coords[1]
        self.flipped = flipped
        self.moving = moving
        if attacking == "True" and (self.attacking == False or self.attacking == "False"):
            self.animate_player.index = 0
        self.attacking = attacking

    def update_pos(self, new_coords, flipped, moving, attacking, delta_time):
        self.interpolation_factor += delta_time

        self.interpolation_factor = min(1.0, max(0.0, self.interpolation_factor))
        interpolated_x = self.interpolate(self.rect.x, new_coords[0], self.interpolation_factor)
        interpolated_y = self.interpolate(self.rect.y, new_coords[1], self.interpolation_factor)

        self.rect.x = interpolated_x
        self.rect.y = interpolated_y

        self.flipped = flipped
        self.moving = moving
        if attacking == "True" and (self.attacking == False or self.attacking == "False"):
            self.animate_player.index = 0
        self.attacking = attacking

    def interpolate(self, start, end, factor):
        return start + (end - start) * factor

    def update(self, unused):
        self.animate_player.animate_other_player(self)