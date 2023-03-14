#map.py
#This file is responsible for loading the map into a usable class

# ----IMPORTS----
import pygame
import json
import os
import sys
import csv

# ----CLASSES----

class Map():
    def __init__(self, map_folder_path, tile_size):
        
        with open(os.path.join(map_folder_path, "MAP_CONFIG.json")) as map_config_file:
            MAP_CONFIG = json.load(map_config_file)
        TILES_CONFIG = MAP_CONFIG["tiles_config"]
    
        #Loading tile images
        tiles_path = os.path.join(map_folder_path, "Tiles")
        TILES = {}
        TILES["H_STRAIGHT"] = pygame.image.load(os.path.join(tiles_path, "H_STRAIGHT.png"))
        TILES["V_STRAIGHT"] = pygame.transform.rotate(TILES["H_STRAIGHT"],90)
        TILES["R_D_TURN"] = pygame.image.load(os.path.join(tiles_path, "R_D_TURN.png"))
        TILES["R_U_TURN"] = pygame.transform.rotate(TILES["R_D_TURN"], -90)
        TILES["L_D_TURN"] = pygame.transform.rotate(TILES["R_D_TURN"], 90)
        TILES["L_U_TURN"] = pygame.transform.rotate(TILES["R_D_TURN"], 180)

        #Loading the map layout
        map_layout = []
        with open(os.path.join(map_folder_path, "MAP_LAYOUT.csv"), newline='') as map_layout_file:
            data = csv.reader(map_layout_file)
            for row in data:
                map_layout.append(row)

        print(map_layout)


        
            



