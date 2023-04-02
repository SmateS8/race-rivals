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
import menu


# ----INIT PYGAME----
pygame.init()
pygame.font.init()

# Set up the screen
if os.name == 'nt': #If you are running windowsw
    ctypes.windll.user32.SetProcessDPIAware() #There is weird bug on larger screen sizes, this will fix that.
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Race Rivals")
# ----VARIABLES----
FPS = 120
# Resolutions & sizes
C_WIDHT, C_HEIGHT =  40,64 #Car size
LOCAL_PLAYER_CAR_IMAGE = os.path.join("Assets","car.png")
MENU_IMAGE_PATH = os.path.join("Assets","MENU_BACKGROUND.png")
COIN_IMAGE_PATH = os.path.join("Assets","COIN.png")


# EXIT = exit the game
# SP_RACE = singleplayer race
# START_MENU = start menu 
# LOGIN_MENU = Login/register menu
MODE = "LOGIN_MENU" # This value holds what should be on the screen right now.


while True:
    if MODE == "START_MENU":
        S_MENU = menu.StartMenu(SCREEN,USERNAME,MENU_IMAGE_PATH,COIN_IMAGE_PATH,FPS)
        MODE,COINS = S_MENU.main_loop()
    if MODE == "LOGIN_MENU":
        L_MENU = menu.LoginMenu(SCREEN,MENU_IMAGE_PATH,FPS)
        MODE,USERNAME = L_MENU.main_loop()

    if MODE == "GARAGE":
        G_MENU = menu.GarageMenu(SCREEN,COINS,USERNAME,MENU_IMAGE_PATH,COIN_IMAGE_PATH,FPS)
        MODE = G_MENU.main_loop()
        
    if MODE == "SP_RACE":
        # run SP_RACE
        SP_Race = race.SinglePlayerRace(USERNAME, car_width=C_WIDHT,car_height=C_HEIGHT,car_image_path=LOCAL_PLAYER_CAR_IMAGE, FPS=FPS, SCREEN=SCREEN)
        SP_Race.countdown()
        SP_Race.main_loop()
        MODE = "START_MENU"
        
    if MODE == "EXIT":
        break


pygame.quit()
sys.exit()

