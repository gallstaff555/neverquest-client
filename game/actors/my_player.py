from game.actors.base_player import BasePlayer
#from game.actors.base_player import BasePlayer
from game.actors.player_action import PlayerAction

class MyPlayer(BasePlayer):
    def __init__(self, name, player_class, race, start_pos, animation_path, animation_frames):
        super().__init__(name, player_class, race, start_pos, animation_path, animation_frames)
        self.player_action = PlayerAction()

    def update(self, collision_group):
        self.animate_player.animate(self)

    def update_pos(self, collision_group, delta_time):
        self.player_action.update_pos(self, self.animate_player, collision_group, delta_time)
