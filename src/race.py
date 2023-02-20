# race.py
# race claases and functions
# Object of the chosen race mode class will be created at main.py main loop and the race will start.


# ----IMPORTS----
import pygame
import os

import json
from car import Car

# ----VARIABLES----
CAR_DATA_PATH = "CAR_DATA.json"

# ----CLASSES----


class SinglePlayerRace():
    def __init__(self, car_width, car_height, car_image_path,FPS):

        with open(CAR_DATA_PATH, 'r') as car_data_file:
            car_data = json.load(car_data_file)
        self.start_x = 50
        # * start_x and start_y will use start tile from the map, as soon as I implement it
        self.start_y = 50
        self.player_car = Car(self.start_x, self.start_y, car_width, car_height,
                              car_data['max_vel'], car_data['acceleration'], car_data['deceleration'], ['rotation_speed'], car_image_path)

        self.car_group = pygame.sprite.Group()
        self.car_group.add(self.player_car)

    def main_loop(self):
        running = True
        while running == True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False


            pygame.display.update()
