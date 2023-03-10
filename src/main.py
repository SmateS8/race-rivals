#main.py
#Runs the game

# ----IMPORTS----
import pygame
import json
import os
import sys
import ctypes

import race
import car


# ----INIT PYGAME----
pygame.init()

# Set up the screen
if os.name == 'nt': #If you are running windows
    ctypes.windll.user32.SetProcessDPIAware() #There is weird bug on larger screen sizes, this will fix that.
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Race Rivals")
# ----VARIABLES----
FPS = 120
# Resolutions & sizes
C_WIDHT, C_HEIGHT =  40,64 #Car size
LOCAL_PLAYER_CAR_IMAGE = os.path.join("Assets","car.png")



# SP_RACE = singleplayer race
# START_MENU = start menu 
MODE = "SP_RACE" # This value holds what should be on the screen right now.


while True:
    if MODE == "SP_RACE":
        # run SP_RACE
        SP_Race = race.SinglePlayerRace(car_width=C_WIDHT,car_height=C_HEIGHT,car_image_path=LOCAL_PLAYER_CAR_IMAGE, FPS=FPS, SCREEN=SCREEN)

        SP_Race.main_loop()
        break


pygame.quit()
sys.exit()

