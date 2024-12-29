#!/usr/bin/env python3 

import socket,threading,json,time

class Client():

    def __init__(self):
        self.connected_to_server = False
        self.other_player_data = {}
        self.npcs = {}

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
        #TODO set self.connect_to_server = False and test

    def sync_server(self, player, server_endpoint, port):
        if (threading.active_count() < 2):
            if not self.connected_to_server:
                #self.connect_to_server()
                header = "connect"
                self.connected_to_server = True
            # TODO prevent more than 2 threads from getting created    
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

    # TODO if connection to server is severed, don't create new messages or threads
    # TODO check for performance improvement and avoid converting string to json object
    def update_server(self, server, port, payload):
        response_obj = json.loads(self.send_message(server, port, f"{payload}"))
        # First element is players; second element is npcs
        self.other_player_data = json.loads(response_obj[0]["players"])
        self.npcs = json.loads(response_obj[1]["npcs"])
        
    def get_data_from_server(self):
        return self.other_player_data
    