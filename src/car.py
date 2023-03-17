#car.py 
#car classes and functions
# ----IMPORTS----
import pygame
import math
# ---------------

# ---- CLASSES ----

# This is the car that will be controled by local user
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, angle,width, height, offroad_vel ,max_vel, acceleration, deceleration, rotation_speed, car_image):
        super().__init__()
        self.original_car = pygame.image.load(car_image)
        self.original_car = pygame.transform.scale(
            self.original_car, (width, height))
        self.image = self.original_car
        self.rect = self.image.get_rect()
        self.prev_rect = self.rect
        self.rect.x = x
        self.rect.y = y
        self.precise_x = x
        self.precise_y = y

        self.vel = 0  # This is the final speed of the car
        self.max_vel = max_vel
        self.velocities = [max_vel, offroad_vel] #Holds default values for both speeds
        self.accel = acceleration
        self.decel = deceleration
        self.rot_speed = rotation_speed
        self.rot = angle  # 0 degrees is car facing down.
        self.speed = [0, 0]
        # -1 to 1, depends on direction. Absolute x + y = 1. Default 0 degrees --> x = 0 ; y = -1
        self.direction = [0, -1]

    def handle_rotation(self, pressed):
        if self.vel > 1:
            if pressed[pygame.K_a]:  # Handling rotation
                self.rot += self.rot_speed
            if pressed[pygame.K_d]:
                self.rot -= self.rot_speed
            if self.rot > 359:
                    self.rot -= 360
            elif self.rot < 0:
                    self.rot += 360  # End of rotation

        # Angle to direction algorith: y direction first
        if self.rot//90 == 0:
            # Using the variable for proxy calculations
            self.direction[1] = 90 - self.rot % 90
            self.direction[1] = round(self.direction[1]/90, 2)
        elif self.rot//90 == 3:
            self.direction[1] = round((self.rot % 90)/90, 2)
        if self.rot//90 == 1:
            self.direction[1] = round((self.rot % 90)/90, 2)
            self.direction[1] = -self.direction[1]
        elif self.rot//90 == 2:
            # Using the variable for proxy calculations
            self.direction[1] = 90 - self.rot % 90
            self.direction[1] = round(self.direction[1]/90, 2)
            self.direction[1] = -self.direction[1]
        self.direction[0] = round(1 - abs(self.direction[1]), 2)
        if 180 <= self.rot <= 359:
            self.direction[0] *= -1

    def handle_forward(self, pressed):
        if pressed[pygame.K_w]: #Acceleration
            if self.vel + self.accel <= self.max_vel:
                self.vel += self.accel
            if self.vel + self.accel > self.max_vel:
                self.vel = self.max_vel
        else: #Deceleration
            if self.vel - self.decel > 0:
                self.vel -= self.decel
            else:
                self.vel = 0    

        # X direction first
        self.speed[0] = self.vel**2 * self.direction[0]  # Using it as a proxy variable
        if self.speed[0] < 0:
            self.speed[0] = math.sqrt(self.speed[0] * (-1))
            self.speed[0] *= (-1)
        else:
            self.speed[0] = math.sqrt(self.speed[0])
        # Y direction second
        self.speed[1] = self.vel**2 * self.direction[1]  # Using it as a proxy variable
        if self.speed[1] < 0:
            self.speed[1] = math.sqrt(self.speed[1] * (-1))
            self.speed[1] *= (-1)
        else:
            self.speed[1] = math.sqrt(self.speed[1])


    def use_offroad_vel(self, offroad):
        if offroad == True:
            self.max_vel = self.velocities[1]
        else:
            self.max_vel = self.velocities[0]

            
    def update(self):
        # Rotating the image
        self.image = pygame.transform.rotozoom(self.original_car, self.rot, 1)
        self.prev_rect = self.rect
        self.rect = self.image.get_rect()
        self.rect.center = self.prev_rect.center
        # Moving the rectangle, and preventing from ecaping the screen
        if self.speed[0] > 0: # X axis
            if not (self.precise_x + self.speed[0] > pygame.display.get_surface().get_width() - self.rect.width/2):
                self.precise_x += self.speed[0]
        elif self.speed[0] < 0:
            if not (self.precise_x + self.speed[0] < 0 + self.rect.width/2):
                self.precise_x += self.speed[0]
        if self.speed[1] > 0: # Y axis
            if not (self.precise_y + self.speed[1] > pygame.display.get_surface().get_height() - self.rect.height/2):
                self.precise_y += self.speed[1]
        elif self.speed[1] < 0:
            if not (self.precise_y + self.speed[1] < 0 + self.rect.height/2):
                self.precise_y += self.speed[1]

        self.rect.centerx = int(self.precise_x)
        self.rect.centery = int(self.precise_y)