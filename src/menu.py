# menu.py
# Classes for different menus


# ----IMPORTS----
import pygame
import pygame_textinput as pg_input
import requests
import os
import json

# ------VARS-----
CAR_DATA_PATH = "CAR_DATA.json"
CAR_UPGRADES_PATH = "CAR_UPGRADES.json"

MAX_PASSWORD_LEN = 12
MAX_USERNAME_LEN = 7

AUTH_SERVER = "http://127.0.0.1:5000"
LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
# -----FUNCs-----


def create_new_car_data(CAR_UPG_PATH, engine_lvl, gearbox_lvl):
    with open(CAR_UPG_PATH, 'r') as f:
        upgrades = json.load(f)
    with open("CAR_DATA.json", 'w') as f:
        data = {

            "max_vel": upgrades['engine_upgrades'][engine_lvl]['top_speed'],
            "offroad_vel": 1.5,
            "acceleration":  upgrades['gearbox_upgrades'][gearbox_lvl]['acceleration'],
            "deceleration": 0.05,
            "rotation_speed": 2,
            "engine_level": engine_lvl,
            "gearbox_level": gearbox_lvl,
            "engine_label": upgrades['engine_upgrades'][engine_lvl]['name'],
            "gearbox_label": upgrades['gearbox_upgrades'][gearbox_lvl]['name']
        }
        json.dump(data, f)


def upgrade_according_to_level(car_data, upgrades):
    data = {

        "max_vel": upgrades['engine_upgrades'][car_data['engine_level']]['top_speed'],
        "offroad_vel": 1.5,
        "acceleration":  upgrades['gearbox_upgrades'][car_data['gearbox_level']]['acceleration'],
        "deceleration": 0.05,
        "rotation_speed": 2,
        "engine_level": car_data['engine_level'],
        "gearbox_level": car_data['gearbox_level'],
        "engine_label": upgrades['engine_upgrades'][car_data['engine_level']]['name'],
        "gearbox_label": upgrades['gearbox_upgrades'][car_data['gearbox_level']]['name']
    }
    return data

# ----CLASSES----


class Button(pygame.sprite.Sprite):

    def __init__(self, text, button_mode, font_name, font_size, color, x, y, width, height):
        super().__init__()
        self.font = pygame.font.SysFont(font_name, font_size)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.text_surface = self.font.render(text, True, pygame.Color("white"))

        # Center the text surface on the button's surface
        text_rect = self.text_surface.get_rect(
            center=self.image.get_rect().center)
        self.image.blit(self.text_surface, text_rect)
        self.button_mode = button_mode

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def return_mode(self):
        return self.button_mode


class StartMenu():
    def __init__(self, SCREEN, USERNAME, MENU_IMAGE_PATH, COIN_IMAGE_PATH, FPS):
        # Show the cursor
        pygame.mouse.set_visible(True)
        # check for the car_data file existion
        # try:
        #     with open(CAR_DATA_PATH, 'r') as f:
        #         pass
        # except FileNotFoundError:
        #     create_new_car_data(CAR_UPGRADES_PATH, 0, 0) #! Replaced by cloud solution

        self.SCREEN = SCREEN
        self.WIDTH, self.HEIGHT = SCREEN.get_size()
        self.MENU_IMAGE = pygame.image.load(MENU_IMAGE_PATH)
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.buttons_width = 200
        self.buttons_height = 75

        font = pygame.font.SysFont('calibri', 64)
        self.COIN = pygame.transform.scale(
            pygame.image.load(COIN_IMAGE_PATH), (64, 64))
        self.COINS = requests.get(
            AUTH_SERVER+'/balance/'+USERNAME).json()['balance']
        self.coin_text_surface = font.render(self.COINS, True, (255, 255, 255))

        self.buttons_labels = ["Singleplayer",
                               "Multiplayer", "Garage", "Quit the game"]
        self.buttons_modes = ["SP_RACE", "MP_RACE", "GARAGE", "EXIT"]
        self.buttons = []
        self.buttons_group = pygame.sprite.Group()
        for index, button_title in enumerate(self.buttons_labels):
            button = Button(button_title, self.buttons_modes[index], "calibri", 25, (
                0, 0, 0), 960-self.buttons_width//2, 50 + index * 100, self.buttons_width, self.buttons_height)
            self.buttons_group.add(button)
            self.buttons.append(button)

    def main_loop(self):
        mode_to_return = ""
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    mode_to_return = "EXIT"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mode_to_return = "EXIT"
                    running = False

                # Check for mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            mode_to_return = button.return_mode()
                            running = False

            self.SCREEN.blit(self.MENU_IMAGE, (0, 0))
            self.buttons_group.draw(self.SCREEN)
            self.SCREEN.blit(self.COIN, (1700, 50))
            self.SCREEN.blit(self.coin_text_surface, (1775, 50))
            #pygame.draw.rect(self.SCREEN, (255,255,255),(785,490,350,100))
            pygame.display.flip()

        return mode_to_return, self.COINS


class LoginMenu():
    def __init__(self, SCREEN, MENU_IMAGE_PATH, FPS):
        # Show the cursor
        pygame.mouse.set_visible(True)

        self.SCREEN = SCREEN
        self.WIDTH, self.HEIGHT = SCREEN.get_size()
        self.MENU_IMAGE = pygame.image.load(MENU_IMAGE_PATH)
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.buttons_width = 200
        self.buttons_height = 75
        self.buttons_group = pygame.sprite.Group()
        # Input Labels
        self.error_font = pygame.font.SysFont("calibri", 36)
        self.error_text_surface = self.error_font.render(
            '', False, (255, 0, 0))
        self.error_position = [1200, 800]

        self.buttons_labels = ["Username", "Password"]
        self.buttons_modes = ["USERNAME", "PASSWORD"]
        buttons_positions = [[760, 440], [760, 540]]
        self.inputs_positions = [[760+220, 440], [760+220, 540]]

        self.input_labels = []
        for index, button_title in enumerate(self.buttons_labels):
            button = Button(button_title, self.buttons_modes[index], "calibri", 25, (
                0, 0, 0), buttons_positions[index][0], buttons_positions[index][1], self.buttons_width, self.buttons_height)
            self.buttons_group.add(button)
            self.input_labels.append(button)

        # Text inputs
        self.active_input = 0  # Username, password. Two inputs are

        manager = pg_input.TextInputManager(
            validator=lambda input: len(input) <= MAX_USERNAME_LEN)
        self.login_username = pg_input.TextInputVisualizer(manager=manager)
        manager = pg_input.TextInputManager(
            validator=lambda input: len(input) <= MAX_PASSWORD_LEN)
        self.login_password = pg_input.TextInputVisualizer(manager=manager)

        self.buttons_labels = ["Login", "Register", "EXIT GAME"]
        # Iam not going to be using modes though, only the "EXIT" one
        self.buttons_modes = ["LOGIN", "REGISTER", "EXIT"]
        buttons_positions = [[750, 800], [970, 800], [860, 900]]

        self.buttons = []
        for index, button_title in enumerate(self.buttons_labels):
            button = Button(button_title, self.buttons_modes[index], "calibri", 25, (
                0, 0, 0), buttons_positions[index][0], buttons_positions[index][1], self.buttons_width, self.buttons_height)
            self.buttons_group.add(button)
            self.buttons.append(button)

    def main_loop(self):
        mode_to_return = ""
        username = ""
        running = True
        while running:
            self.clock.tick(self.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    mode_to_return = "EXIT"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mode_to_return = "EXIT"
                    running = False

                # Check for mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    for label in self.input_labels:
                        if label.is_clicked(mouse_pos):
                            active_input_label = label.return_mode()
                            if active_input_label == "USERNAME":
                                self.active_input = 0
                            elif active_input_label == "PASSWORD":
                                self.active_input = 1

                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            mode_to_return = button.return_mode()
                            if mode_to_return == "EXIT":
                                running = False
                            elif mode_to_return == "LOGIN":
                                username = self.login_username.value
                                password = self.login_password.value
                                data = {
                                    "username": username,
                                    "password": password
                                }
                                response = requests.get(
                                    AUTH_SERVER+LOGIN_ENDPOINT, json=data)
                                if response.json() == True:
                                    running = False
                                    mode_to_return = "START_MENU"
                                else:
                                    self.error_text_surface = self.error_font.render(
                                        'Incorrect login', False, (255, 0, 0))
                            elif mode_to_return == "REGISTER":
                                username = self.login_username.value
                                password = self.login_password.value
                                data = {
                                    "username": username,
                                    "password": password
                                }
                                response = requests.post(
                                    AUTH_SERVER+REGISTER_ENDPOINT, json=data)
                                if response.json() == True:
                                    running = False
                                    mode_to_return = "START_MENU"
                                elif response.json()["message"] == "special chars":
                                    self.error_text_surface = self.error_font.render(
                                        'Can\'t contain special characters', False, (255, 0, 0))
                                elif response.json()["message"] == "username exists":
                                    self.error_text_surface = self.error_font.render(
                                        'This username is already taken', False, (255, 0, 0))

            if self.active_input == 0:
                self.login_username.update(events)
            else:
                self.login_password.update(events)

            self.SCREEN.blit(self.MENU_IMAGE, (0, 0))
            self.buttons_group.draw(self.SCREEN)
            self.SCREEN.blit(self.login_username.surface,
                             (self.inputs_positions[0][0], self.inputs_positions[0][1]))
            self.SCREEN.blit(self.login_password.surface,
                             (self.inputs_positions[1][0], self.inputs_positions[1][1]))
            self.SCREEN.blit(self.error_text_surface,
                             tuple(self.error_position))
            #pygame.draw.rect(self.SCREEN, (255,255,255),(785,490,350,100))
            pygame.display.flip()
        return mode_to_return, username


class GarageMenu():
    def __init__(self, SCREEN, COINS, USERNAME, MENU_IMAGE_PATH, COIN_IMAGE_PATH, FPS):
        # Show the cursor
        pygame.mouse.set_visible(True)

        self.SCREEN = SCREEN
        self.WIDTH, self.HEIGHT = SCREEN.get_size()
        self.MENU_IMAGE = pygame.image.load(MENU_IMAGE_PATH)
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.buttons_width = 200
        self.buttons_height = 75
        self.USERNAME = USERNAME
        self.car_data = requests.get(AUTH_SERVER+'/car/'+ USERNAME).json()
        with open(CAR_UPGRADES_PATH, 'r') as f:
            self.car_upgrades = json.load(f)

        font = pygame.font.SysFont('roboto', 40)
        labels_color = (0, 0, 0)
        self.upgrade_font = font
        self.upgrade_count_pos = [(960, 120), (960, 420)]  # Engine, gearbox
        self.labels = [font.render("Engine Upgrade", True, labels_color), font.render(
            "Gearbox Upgrade", True, labels_color)]
        self.labels_positions = [(175, 120), (175, 420)]

        self.font = pygame.font.SysFont('calibri', 64)
        self.COIN = pygame.transform.scale(
            pygame.image.load(COIN_IMAGE_PATH), (64, 64))
        self.COINS = int(COINS)
        self.coin_text_surface = self.font.render(str(self.COINS), True, (255, 255, 255))

        self.buttons_labels = ["Buy", "Buy", "Quit to menu"]
        self.buttons_modes = ["ENGINE_UPGRADE",
                              "GEARBOX_UPGRADE", "START_MENU"]
        self.buttons_positions = [[500, 100], [
            500, 400], [750, 800], [970, 800]]
        self.buttons = []
        self.buttons_group = pygame.sprite.Group()
        for index, button_title in enumerate(self.buttons_labels):
            button = Button(button_title, self.buttons_modes[index], "calibri", 25, (
                0, 0, 0), self.buttons_positions[index][0], self.buttons_positions[index][1], self.buttons_width, self.buttons_height)
            self.buttons_group.add(button)
            self.buttons.append(button)

    def main_loop(self):
        mode_to_return = ""
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    mode_to_return = "EXIT"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mode_to_return = "EXIT"
                    running = False

                # Check for mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            mode_to_return = button.return_mode()
                            if mode_to_return == "START_MENU":
                                running = False
                            if mode_to_return == "ENGINE_UPGRADE"  and self.car_data['engine_level'] < (len(self.car_upgrades['engine_upgrades'])-1) and int(self.COINS) >= self.car_upgrades['engine_upgrades'][self.car_data['engine_level']+1]['price']:
                                self.COINS -= self.car_upgrades['engine_upgrades'][self.car_data['engine_level']+1]['price']
                                self.car_data['engine_level'] += 1
                                self.car_data = upgrade_according_to_level(self.car_data, self.car_upgrades)
                                self.coin_text_surface = self.font.render(str(self.COINS), True, (255, 255, 255))

                            if mode_to_return == "GEARBOX_UPGRADE" and self.car_data['gearbox_level'] < len(self.car_upgrades['gearbox_upgrades'])-1 and int(self.COINS) >= self.car_upgrades['gearbox_upgrades'][self.car_data['gearbox_level']+1]['price']:
                                self.COINS -= self.car_upgrades['gearbox_upgrades'][self.car_data['gearbox_level']+1]['price']
                                self.car_data['gearbox_level'] += 1
                                self.car_data = upgrade_according_to_level(self.car_data, self.car_upgrades)
                                self.coin_text_surface = self.font.render(str(self.COINS), True, (255, 255, 255))

            self.SCREEN.blit(self.MENU_IMAGE, (0, 0))
            self.buttons_group.draw(self.SCREEN)
            self.SCREEN.blit(self.COIN, (1700, 50))
            self.SCREEN.blit(self.coin_text_surface, (1775, 50))
            for index, label in enumerate(self.labels):
                self.SCREEN.blit(label, self.labels_positions[index])
            label = self.upgrade_font.render(
                f"{self.car_data['engine_level']}/{len(self.car_upgrades['engine_upgrades'])-1}.    You have {self.car_data['engine_label']}", True, (0, 0, 0))
            self.SCREEN.blit(label, self.upgrade_count_pos[0])
            label = self.upgrade_font.render(
                f"{self.car_data['gearbox_level']}/{len(self.car_upgrades['gearbox_upgrades'])-1}.    You have {self.car_data['gearbox_label']}", True, (0, 0, 0))
            self.SCREEN.blit(label, self.upgrade_count_pos[1])
            #pygame.draw.rect(self.SCREEN, (255,255,255),(785,490,350,100))
            pygame.display.flip()
        requests.post(AUTH_SERVER+'/car/'+ self.USERNAME, json=self.car_data)
        requests.post(AUTH_SERVER+'/balance/set/'+self.USERNAME+'/'+str(self.COINS))
        return mode_to_return
