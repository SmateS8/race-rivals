# race.py
# race claases and functions
# Object of the chosen race mode class will be created at main.py main loop and the race will start.


# ----IMPORTS----
import pygame
import os

import json
from car import Car
from map import Map

# ----VARIABLES----
CAR_DATA_PATH = "CAR_DATA.json"
MAP1_FOLDER_PATH = os.path.join("Assets","Maps", "MAP1")
# ----CLASSES----


class SinglePlayerRace():
    def __init__(self, car_width, car_height, car_image_path,FPS,SCREEN):
        #Hiding mouse cursor
        pygame.mouse.set_visible(False)
        #Screen VARs
        self.SCREEN = SCREEN
        self.FPS = FPS
        self.clock = pygame.time.Clock()


        with open(CAR_DATA_PATH, 'r') as car_data_file:
            car_data = json.load(car_data_file)

        self.start_x = 50
        # * start_x and start_y will use start tile from the map, as soon as I implement it
        self.start_y = 50
        self.player_car = Car(self.start_x, self.start_y, car_width, car_height,
                              car_data['max_vel'], car_data['acceleration'], car_data['deceleration'], car_data['rotation_speed'], car_image_path)

        self.car_group = pygame.sprite.Group()
        self.car_group.add(self.player_car)

        #Creating Map
        self.map = Map(MAP1_FOLDER_PATH, 120, self.SCREEN)

    def main_loop(self):
        racing = True
        while racing == True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    racing = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    racing = False
            # Handle user input
            pressed_keys = pygame.key.get_pressed()
            self.player_car.handle_rotation(pressed_keys)
            self.player_car.handle_forward(pressed_keys)

            # Draw the screen background
            self.SCREEN.fill((255, 255, 255)) 
            self.car_group.update()
            self.SCREEN.blit(self.map.map_surface,(0,0))
            self.car_group.draw(self.SCREEN)            

            pygame.display.flip()
