#menu.py
#Classes for different menus



# ----IMPORTS----
import pygame
import pygame_textinput as pg_input
import requests

# ------VARS-----
MAX_PASSWORD_LEN = 12
MAX_USERNAME_LEN = 7

AUTH_SERVER = "http://localhost:5000"
LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"

# ----CLASSES----

class Button(pygame.sprite.Sprite):

    def __init__(self, text, button_mode, font_name, font_size, color, x, y, width, height):
        super().__init__()
        self.font = pygame.font.SysFont(font_name,font_size)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.text_surface = self.font.render(text, True, pygame.Color("white"))

        # Center the text surface on the button's surface
        text_rect = self.text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.text_surface, text_rect)
        self.button_mode = button_mode

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def return_mode(self):
        return self.button_mode

class StartMenu():
    def __init__(self,SCREEN,MENU_IMAGE_PATH,FPS):
        #Show the cursor
        pygame.mouse.set_visible(True)

        self.SCREEN = SCREEN
        self.WIDTH, self.HEIGHT = SCREEN.get_size()
        self.MENU_IMAGE = pygame.image.load(MENU_IMAGE_PATH)
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.buttons_width = 200
        self.buttons_height = 75

        self.buttons_labels = ["Singleplayer","Multiplayer","Garage","Quit the game"]
        self.buttons_modes = ["SP_RACE","MP_RACE","GARAGE","EXIT"]
        self.buttons = []
        self.buttons_group = pygame.sprite.Group()
        for index, button_title in enumerate(self.buttons_labels):
            button = Button(button_title, self.buttons_modes[index],"calibri",25,(0,0,0),960-self.buttons_width//2, 50 + index * 100,self.buttons_width,self.buttons_height)
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

            self.SCREEN.blit(self.MENU_IMAGE,(0,0))
            self.buttons_group.draw(self.SCREEN)
            #pygame.draw.rect(self.SCREEN, (255,255,255),(785,490,350,100))
            pygame.display.flip()
        
        
        
        return mode_to_return
    

class LoginMenu():
    def __init__(self,SCREEN,MENU_IMAGE_PATH,FPS):
        #Show the cursor
        pygame.mouse.set_visible(True)

        self.SCREEN = SCREEN
        self.WIDTH, self.HEIGHT = SCREEN.get_size()
        self.MENU_IMAGE = pygame.image.load(MENU_IMAGE_PATH)
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.buttons_width = 200
        self.buttons_height = 75
        self.buttons_group = pygame.sprite.Group()
        #Input Labels
        self.error_font = pygame.font.SysFont("calibri",36)
        self.error_text_surface = self.error_font.render('', False, (255, 0, 0))
        self.error_position = [1200,800]

        self.buttons_labels = ["Username","Password"]
        self.buttons_modes = ["USERNAME","PASSWORD"]
        buttons_positions = [[760,440],[760,540]]
        self.inputs_positions = [[760+220,440],[760+220,540]]


        self.input_labels = []
        for index, button_title in enumerate(self.buttons_labels):
            button = Button(button_title, self.buttons_modes[index],"calibri",25,(0,0,0),buttons_positions[index][0],buttons_positions[index][1],self.buttons_width,self.buttons_height)
            self.buttons_group.add(button)
            self.input_labels.append(button)

        #Text inputs
        self.active_input = 0# Username, password. Two inputs are 

        manager = pg_input.TextInputManager(validator = lambda input: len(input) <= MAX_USERNAME_LEN)
        self.login_username = pg_input.TextInputVisualizer(manager=manager)
        manager = pg_input.TextInputManager(validator = lambda input: len(input) <= MAX_PASSWORD_LEN)
        self.login_password = pg_input.TextInputVisualizer(manager=manager)

        self.buttons_labels = ["Login","Register","EXIT GAME"]
        self.buttons_modes = ["LOGIN","REGISTER", "EXIT"] #Iam not going to be using modes though, only the "EXIT" one
        buttons_positions = [[750,800],[970,800],[860,900]]

        self.buttons = []
        for index, button_title in enumerate(self.buttons_labels):
            button = Button(button_title, self.buttons_modes[index],"calibri",25,(0,0,0),buttons_positions[index][0],buttons_positions[index][1],self.buttons_width,self.buttons_height)
            self.buttons_group.add(button)
            self.buttons.append(button)


    

    def main_loop(self):
        mode_to_return = ""
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
                                        "username":username,
                                        "password":password
                                    }
                                    response = requests.get(AUTH_SERVER+LOGIN_ENDPOINT,json = data)
                                    if response.json() == True:
                                        running = False
                                        mode_to_return = "START_MENU"
                                    else:
                                        self.error_text_surface = self.error_font.render('Incorrect login', False, (255, 0, 0))
                                elif mode_to_return == "REGISTER":
                                    username = self.login_username.value
                                    password = self.login_password.value
                                    data = {
                                        "username":username,
                                        "password":password
                                    }
                                    response = requests.post(AUTH_SERVER+REGISTER_ENDPOINT,json = data)
                                    if response.json() == True:
                                        running = False
                                        mode_to_return = "START_MENU"
                                    elif response.json()["message"] == "special chars":
                                        self.error_text_surface = self.error_font.render('Can\'t constain special characters', False, (255, 0, 0))
                                    elif response.json()["message"] == "username exists":
                                        self.error_text_surface = self.error_font.render('This username is already taken', False, (255, 0, 0))                                       




            if self.active_input == 0:
                self.login_username.update(events)
            else:
                self.login_password.update(events)

            self.SCREEN.blit(self.MENU_IMAGE,(0,0))
            self.buttons_group.draw(self.SCREEN)
            self.SCREEN.blit(self.login_username.surface, (self.inputs_positions[0][0], self.inputs_positions[0][1]))
            self.SCREEN.blit(self.login_password.surface, (self.inputs_positions[1][0], self.inputs_positions[1][1]))
            self.SCREEN.blit(self.error_text_surface,tuple(self.error_position))
            #pygame.draw.rect(self.SCREEN, (255,255,255),(785,490,350,100))
            pygame.display.flip()
        
        
        
        return mode_to_return




