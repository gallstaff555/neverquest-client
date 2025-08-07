import ast, json
from game.config.config import Config 
from game.actors.other_player import OtherPlayer
from game.actors.npc import NPC

cfg = Config()

class PlayerNPCTracker():
    def __init__(self, my_player, camera_group):
        self.player = my_player
        self.camera_group = camera_group
        self.other_players = {}
        self.npcs = {}

    def update_other_players(self, data, delta_time):
        for key in data:
            if key == self.player.name:
                pass
            elif key in self.other_players:
                self.other_players[key].update_pos(data[key]["pos"], data[key]["flipped"], data[key]["moving"], data[key]["attacking"], delta_time)
            else: # add new player
                print(f"New player {key} joined.")
                race = data[key]["race"]
                player_class = data[key]["player_class"]
                # TODO standardize colors
                if race == "elf":
                    color = 3
                elif race == "human":
                    color = 1
                animation_path = f"../assets/{race}/{player_class}/color_{color}"
                new_player = OtherPlayer(key, data[key]["player_class"], data[key]["race"], data[key]["pos"], animation_path, cfg.DEFAULT_ANIMATIONS)
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

    def update_npcs(self, data, delta_time):
        for key in data:
            npc = json.loads(data[key])
            if key in self.npcs:
                self.npcs[key].update_pos(ast.literal_eval(npc["pos"]), npc["flipped"], npc["moving"], npc["attacking"], delta_time)
            else: 
            # add new npc
                print(f"New NPC id:{key} added.")
                #race = data[key]["race"]
                race = npc["race"]
                #player_class = data[key]["player_class"]
                npc_class = npc["npc_class"]
                # TODO standardize colors
                if race == "elf":
                    color = 3
                elif race == "human":
                    color = 1
                animation_path = f"../assets/{race}/{npc_class}/color_{color}"

                new_npc = NPC(key, npc_class, race, ast.literal_eval(npc["pos"]), animation_path, cfg.DEFAULT_ANIMATIONS)
                self.npcs[key] = new_npc
                self.camera_group.add(new_npc)