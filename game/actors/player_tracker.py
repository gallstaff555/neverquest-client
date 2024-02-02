import ast 
from game.config.config import Config 
from game.actors.other_player import OtherPlayer

cfg = Config()

class PlayerTracker():
    def __init__(self, my_player, camera_group):
        self.player = my_player
        self.camera_group = camera_group
        self.other_players = {}

    def update_other_players(self, data, delta_time):
        for key in data:
            if key == self.player.name:
                pass
            elif key in self.other_players:
                self.other_players[key].update_pos(ast.literal_eval(data[key]["pos"]), data[key]["flipped"], data[key]["moving"], data[key]["attacking"], delta_time)
            else: # add new player
                print(f"New player {key} joined.")
                race = data[key]["race"]
                player_class = data[key]["player_class"]
                color = 3
                animation_path = f"../assets/{race}/{player_class}/color_{color}"
                new_player = OtherPlayer(key, data[key]["player_class"], data[key]["race"], ast.literal_eval((data[key]["pos"])), animation_path, cfg.DEFAULT_ANIMATIONS)
                self.other_players[key] = new_player
                self.camera_group.add(new_player)
        # look for players that disconnected by comparing players to keys not found
        players_to_delete = []
        for player in self.other_players:  
            if player not in data:
                print(f"{player} is no longer connected!")
                players_to_delete.append(player)
        for player in players_to_delete:  
            delete_player = self.other_players[player]
            self.camera_group.remove(delete_player)
            del self.other_players[player]