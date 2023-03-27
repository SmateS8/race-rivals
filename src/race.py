# race.py
# race claases and functions
# Object of the chosen race mode class will be created at main.py main loop and the race will start.


# ----IMPORTS----
import pygame
import os
import time

import json
from car import Car
from map import Map

# ----VARIABLES----
CAR_DATA_PATH = "CAR_DATA.json"
MAP1_FOLDER_PATH = os.path.join("Assets","Maps", "MAP1")
TILE_SIZE = 120
# ----CLASSES----


class SinglePlayerRace():
    def __init__(self, car_width, car_height, car_image_path,FPS,SCREEN):
        #Hiding mouse cursor
        pygame.mouse.set_visible(False)
        #Screen VARs
        self.SCREEN = SCREEN
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.SCREEN.get_size()
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        self.laps_font = pygame.font.SysFont("Comic Sans MS", 64)

        self.lap_count = 0
        self.max_laps = 3

        #Creating Map
        self.map = Map(MAP1_FOLDER_PATH, TILE_SIZE, self.SCREEN)
        self.checkpoints = self.map.checkpoints
        self.finish_rect = pygame.Rect(self.map.start_finish_tile[0],self.map.start_finish_tile[1],TILE_SIZE,TILE_SIZE)
        self.start_x = self.map.start_finish_tile[0] + TILE_SIZE/2 
        self.start_y = self.map.start_finish_tile[1] + TILE_SIZE/2 

        with open(CAR_DATA_PATH, 'r') as car_data_file:
            car_data = json.load(car_data_file)


        self.player_car = Car(self.start_x, self.start_y,self.map.car_start_angle, car_width, car_height, car_data['offroad_vel'],
                              car_data['max_vel'], car_data['acceleration'], car_data['deceleration'], car_data['rotation_speed'], car_image_path)

        self.car_group = pygame.sprite.Group()
        self.car_group.add(self.player_car)


    def countdown(self):
        strings = ["3","2","1","GO!"]

        self.SCREEN.fill((255, 255, 255)) # Drawing some bg, on top of which there will be a count down  
        self.SCREEN.blit(self.map.map_surface,(0,0))
        self.car_group.update()
        self.car_group.draw(self.SCREEN) 
        pygame.display.flip()
        font = pygame.font.SysFont("Comic Sans MS", 120)
        for count in range(4):
            self.SCREEN.fill((255, 255, 255))
            self.SCREEN.blit(self.map.map_surface,(0,0))
            self.car_group.update()
            self.car_group.draw(self.SCREEN) 


            text = font.render(strings[count],True,(255,255,255))
            pos_rect = text.get_rect(center=(self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2))
            self.SCREEN.blit(text,pos_rect)

            pygame.display.update()
            pygame.time.wait(900)


    def main_loop(self):
        start_time = time.time()
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

            #Handle car off-roading
            offroad = False
            for rect in self.map.slow_down_tiles:
                if rect.collidepoint(self.player_car.rect.center):
                    offroad = True
            self.player_car.use_offroad_vel(offroad)
            #Handle checkpoint crossing
            for checkblock in self.checkpoints:
                for block in checkblock[0]:
                    if block.colliderect(self.player_car.rect):
                        checkblock[1] = True
            #Handle new lap
            if self.finish_rect.colliderect(self.player_car):
                passed_checkpoints = True
                for check in self.checkpoints:
                    if check[1] == False:
                        passed_checkpoints = False
                if passed_checkpoints:
                    if self.lap_count + 1 < self.max_laps:
                        self.lap_count += 1
                        self.checkpoints = self.map.restore_checkpoints(self.checkpoints)
                        #print(self.checkpoints)
                    else:
                        print(f"You won in {round(time.time()-start_time)} seconds")
                        racing = False


            lap_text = f"{self.lap_count}/{self.max_laps} laps"
            lap_text_surface = self.laps_font.render(lap_text, True, pygame.Color("white"))
            lap_rect = lap_text_surface.get_rect(center=(self.SCREEN_WIDTH//2, 50))

            # Draw the screen
            self.SCREEN.fill((255, 255, 255)) 
            self.car_group.update()
            self.SCREEN.blit(self.map.map_surface,(0,0))
            self.car_group.draw(self.SCREEN)
            self.SCREEN.blit(lap_text_surface, lap_rect)

            checkpoints = self.map.checkpoints #* Draws checkpoints 
            for checkblock in checkpoints:
               for i in checkblock[0]:
                  pygame.draw.rect(self.SCREEN,(255,255,255),i)            
            # pygame.draw.rect(self.SCREEN,(0,0,0),self.finish_rect ) #* Draws finish block
            pygame.display.flip()
