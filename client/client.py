#!/usr/bin/env python3 

import socket,threading,json,time

class Client():

    def __init__(self):
        self.connected_to_server = False
        self.data_from_server = {}

    def send_message(self, host, port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(bytes(message, "utf-8"))
            response = sock.recv(2048)
            return response.decode("utf-8")
        
    def disconnect_from_server(self, my_player, server, port):
        payload = {
            "header": "disconnect",
            "name": f"{my_player}"
        }
        thread = threading.Thread(target=self.update_server, args=(server, port, payload,))
        thread.start()

    def sync_server(self, player, server_endpoint, port):
        if (threading.active_count() < 2):
            if not self.connected_to_server:
                #self.connect_to_server()
                header = "connect"
                self.connected_to_server = True
            else:
                header = "update"
                payload = {
                    "header": f"{header}",
                    "name": f"{player.name}",
                    "player_class": f"{player.player_class}",
                    "race": f"{player.race}",
                    "pos": f"{(player.rect.x, player.rect.y)}",
                    "flipped": f"{player.flipped}",
                    "appearance": f"{player.race}", 
                    "moving": f"{player.moving}",
                    "attacking": f"{player.attacking}",
                    "last_update": f"{int(time.time())}"
                }
                thread = threading.Thread(target=self.update_server, args=(server_endpoint, port, payload,))
                thread.start()

    def update_server(self, server, port, payload):
        self.data_from_server = json.loads(self.send_message(server, port, f"{payload}"))
        
    def get_data_from_server(self):
        return self.data_from_server
    
    # def update_other_players(self, data, delta_time, my_player, other_players, camera_group, animations):
    #     for key in data:
    #         if key == my_player:
    #             pass
    #         elif key in other_players:
    #             other_players[key].update_pos(ast.literal_eval(data[key]["pos"]), data[key]["flipped"], data[key]["moving"], data[key]["attacking"], delta_time)
    #         else: # add new player
    #             print(f"New player {key} joined.")
    #             race = data[key]["race"]
    #             player_class = data[key]["player_class"]
    #             color = 3
    #             animation_path = f"../assets/{race}/{player_class}/color_{color}"
    #             new_player = OtherPlayer(key, data[key]["player_class"], data[key]["race"], ast.literal_eval((data[key]["pos"])), animation_path, animations)
    #             other_players[key] = new_player
    #             camera_group.add(new_player)

    #     # look for players that disconnected by comparing players to keys not found
    #     players_to_delete = []
    #     for player in other_players:  
    #         if player not in data:
    #             print(f"{player} is no longer connected!")
    #             players_to_delete.append(player)
    #     for player in players_to_delete:  
    #         delete_player = other_players[player]
    #         camera_group.remove(delete_player)
    #         del other_players[player]