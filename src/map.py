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
    def __init__(self, map_folder_path, tile_size, SCREEN):
        self.TILE_SIZE = tile_size
        self.SCREEN = SCREEN
        self.SCREEN_SURFACE = pygame.display.get_surface()

        with open(os.path.join(map_folder_path, "MAP_CONFIG.json")) as map_config_file:
            MAP_CONFIG = json.load(map_config_file)
        self.TILES_CONFIG = MAP_CONFIG["tiles_config"]

        self.car_start_angle = MAP_CONFIG['car_start_angle'] # Used in race.py for start angle

        #Loading tile images
        tiles_path = os.path.join(map_folder_path, "Tiles")
        self.TILES = {}
        self.TILES["H_STRAIGHT"] = pygame.image.load(os.path.join(tiles_path, "H_STRAIGHT.png"))
        self.TILES["V_STRAIGHT"] = pygame.transform.rotate(self.TILES["H_STRAIGHT"],90)
        self.TILES["R_D_TURN"] = pygame.image.load(os.path.join(tiles_path, "R_D_TURN.png"))
        self.TILES["R_U_TURN"] = pygame.transform.rotate(self.TILES["R_D_TURN"], 90)
        self.TILES["L_D_TURN"] = pygame.transform.rotate(self.TILES["R_D_TURN"], -90)
        self.TILES["L_U_TURN"] = pygame.transform.rotate(self.TILES["R_D_TURN"], 180)
        self.TILES["SLOW_DOWN_BG"] = pygame.image.load(os.path.join(tiles_path, "SLOW_DOWN_BG.png"))
        self.TILES["START_FINISH"] = pygame.image.load(os.path.join(tiles_path, "START_FINISH.png"))
        #Resizing Tiles
        for tile in self.TILES:
            self.TILES[tile] = pygame.transform.scale(self.TILES[tile],(self.TILE_SIZE, self.TILE_SIZE))

        #Loading the map layout
        self.map_layout = []
        with open(os.path.join(map_folder_path, "MAP_LAYOUT.csv"), newline='') as map_layout_file:
            data = csv.reader(map_layout_file)
            for row in data:
                self.map_layout.append(row)

        #Loading map layout into surface
        self.slow_down_tiles = [] # List of rectangle on which when collided the car will slow down
        self.map_surface = pygame.Surface((self.SCREEN_SURFACE.get_width(),self.SCREEN_SURFACE.get_height()))
        row_index = 0
        for row in self.map_layout:
            column_index = 0 
            for column in row:
                Tile_name = list(self.TILES_CONFIG.keys())[list(self.TILES_CONFIG.values()).index(int(column))]
                self.map_surface.blit(self.TILES[Tile_name], (self.TILE_SIZE * column_index, self.TILE_SIZE * row_index))
                if Tile_name == 'SLOW_DOWN_BG':
                    self.slow_down_tiles.append(pygame.Rect((self.TILE_SIZE * column_index, self.TILE_SIZE * row_index), (tile_size,tile_size)))
                if Tile_name == 'START_FINISH':
                    self.start_finish_tile = [self.TILE_SIZE*column_index, self.TILE_SIZE*row_index]
                column_index +=1
            row_index +=1


