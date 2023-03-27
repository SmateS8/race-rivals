#menu.py
#Classes for different menus



# ----IMPORTS----
import pygame
import os

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




