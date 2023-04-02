# race.py
# race claases and functions
# Object of the chosen race mode class will be created at main.py main loop and the race will start.


# ----IMPORTS----
import pygame
import os
import time

import requests
import json
from car import Car
from map import Map

# ----VARIABLES----
CAR_API = 'http://127.0.0.1:5000/car/'
API = 'http://127.0.0.1:5000'
MULTIPLAYER_SERVER = ('127.0.0.1',5555)

MAP1_FOLDER_PATH = os.path.join("Assets","Maps", "MAP1")
TILE_SIZE = 120
# ----CLASSES----


class SinglePlayerRace():
    def __init__(self, username ,car_width, car_height, car_image_path,FPS,SCREEN):
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

        car_data = requests.get(CAR_API+username).json()


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
            # pygame.draw.rect(self.SCREEN,(0,0,0),self.finish_rect ) #* Draws finish block
            pygame.display.flip()


class MultiPlayerRace():
    def __init__(self, username ,coins,car_width, car_height, car_image_path,FPS,SCREEN):
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
        self.USERNAME = username
        #Creating Map
        self.map = Map(MAP1_FOLDER_PATH, TILE_SIZE, self.SCREEN)
        self.checkpoints = self.map.checkpoints
        self.finish_rect = pygame.Rect(self.map.start_finish_tile[0],self.map.start_finish_tile[1],TILE_SIZE,TILE_SIZE)
        self.start_x = self.map.start_finish_tile[0] + TILE_SIZE/2 
        self.start_y = self.map.start_finish_tile[1] + TILE_SIZE/2 

        car_data = requests.get(CAR_API+username).json()
        self.COINS = coins

        self.player_car = Car(self.start_x, self.start_y,self.map.car_start_angle, car_width, car_height, car_data['offroad_vel'],
                              car_data['max_vel'], car_data['acceleration'], car_data['deceleration'], car_data['rotation_speed'], car_image_path)

        self.car_group = pygame.sprite.Group()
        self.car_group.add(self.player_car)

    def wait_for_players(self):

        font = pygame.font.SysFont("Comic Sans MS", 64)
        waiting_text = font.render('Waiting for player...', True, (255,255,255))
        against_text = font.render(f'{self.USERNAME} vs. ', True, (255,255,255))
        waiting = True
        exit_game = False
        lobby = requests.get(API+'/lobby/create/'+self.USERNAME).json()['lobby']
        lobby_id = lobby['id']
        self.lobby_id = lobby_id
        while waiting:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    waiting = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    exit_game = True
            lobby = requests.get(API+'/lobby/check/'+str(lobby_id)).json()['lobby']
            print(lobby)
            if lobby['player1'] == self.USERNAME:
                opponent_name = lobby["player2"]
            else:
                opponent_name = lobby["player1"]
            against_text = font.render(f'{self.USERNAME} vs. {opponent_name}', True, (255,255,255))
            self.SCREEN.fill((0,0,0))
            self.SCREEN.blit(waiting_text,waiting_text.get_rect(center=(self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2)))
            self.SCREEN.blit(against_text,against_text.get_rect(center=(self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2+100)))
            pygame.display.flip()
            pygame.time.wait(900)
            if opponent_name != "":
                pygame.time.wait(1000)
                waiting = False
    def wait_for_opponent_finish(self):

        font = pygame.font.SysFont("Comic Sans MS", 64)
        waiting_text = font.render('Waiting for player to finish...', True, (255,255,255))
        won_text = font.render('You won 5 coins!!', True, (255,255,255))
        lost_text = font.render('You have lost 3 coins :(', True, (255,255,255))
        against_text = font.render(f'Your time: {self.PLAYER_TIME} vs. ', True, (255,255,255))
        waiting = True
        lobby_id = self.lobby_id
        while waiting:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    waiting = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    exit_game = True
            lobby = requests.get(API+'/lobby/check/'+str(lobby_id)).json()['lobby']
            if lobby['player1'] == self.USERNAME:
                opponent_time = lobby["player2_time"]
            else:
                opponent_time = lobby["player1_time"]
            if not opponent_time == 0:
                against_text = font.render(f'Your time: {self.PLAYER_TIME} vs. {opponent_time}', True, (255,255,255))
            self.SCREEN.fill((0,0,0))
            self.SCREEN.blit(waiting_text,waiting_text.get_rect(center=(self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2)))
            self.SCREEN.blit(against_text,against_text.get_rect(center=(self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2+100)))
            pygame.display.flip()
            pygame.time.wait(900)
            if opponent_time != 0:
                if self.PLAYER_TIME > opponent_time:
                    self.SCREEN.blit(lost_text,lost_text.get_rect(center=(self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2+200)))
                    requests.post(API+'/balance/set/'+self.USERNAME+'/'+str(int(self.COINS) - 3))
                else:
                    self.SCREEN.blit(won_text,won_text.get_rect(center=(self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2+200)))
                    requests.post(API+'/balance/set/'+self.USERNAME+'/'+str(int(self.COINS) + 5))
                pygame.display.flip()
                pygame.time.wait(1500)
                waiting = False
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
            # pygame.draw.rect(self.SCREEN,(0,0,0),self.finish_rect ) #* Draws finish block
            pygame.display.flip()
        self.PLAYER_TIME = round(time.time()-start_time,2)
        timebz, timeaz = str(self.PLAYER_TIME).split('.')
        response = requests.get(API + '/lobby/time/'+str(self.lobby_id)+'/'+self.USERNAME+'/'+timebz+'/'+timeaz)

