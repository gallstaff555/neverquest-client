#!/usr/bin/env python3

#TODO 
#FEATURES
#Add animation 
#Game server needs to detect if a player disconnected
#Load levels dynamically, rather than hardcode level data in main.py
#Load all animations only once, not when player is created
#handle case where player alt+f4 or ctrl-c to close their game
#add mouse/target reticle 
#experiment with rotating sprite 90 degrees 
#send full player info during connection, not during update message


import argparse
from game.game import Game

if __name__ == '__main__':
    #create character with given name, race and color

    parser = argparse.ArgumentParser(description='Game client arguments')
    parser.add_argument('--name', type=str, default="default_name", required=True)
    parser.add_argument('--player_class', type=str, default="archer", required=True)
    parser.add_argument('--race', type=str, default="elf", required=True)
    parser.add_argument('--color', type=str, default="3", required=True)
    args = parser.parse_args()
    game = Game(args.name, args.player_class, args.race, args.color)
    value = game.start_game()