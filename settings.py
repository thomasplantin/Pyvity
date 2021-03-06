import pygame
import math
import constants

class Ball:
    def __init__(self, color=(0, 0, 0), center=(400, 250), radius=20):
        self.color = color
        self.center = center
        self.radius = radius

    def draw(self, window):
        pygame.draw.circle(window, (0, 0, 0), self.center, self.radius)
        pygame.draw.circle(window, self.color, self.center, self.radius - 1)

    @staticmethod
    def ball_path(start_x_y, vectors, time, gravity):
        velocity_x = vectors[0] * (1 - constants.PERCENTAGE_HANDICAP)
        velocity_y = vectors[1] * (1 - constants.PERCENTAGE_HANDICAP)
        dist_x = velocity_x * time
        dist_y = velocity_y * time + 0.5 * gravity * math.pow(time, 2)
        return (round(start_x_y[0] + dist_x), round(start_x_y[1] + dist_y))

    def check_boundaries(self, start_x_y, vectors):
        if self.center[0] <= self.radius:
            # If the ball travels out of the window to the left
            offset = - start_x_y[0]
            start_x_y[0] = offset + self.radius 
            vectors[0] = -vectors[0]
        elif self.center[0] >= constants.WINDOW_WIDTH - self.radius:
            # If the ball travels out of the window to the right
            offset = constants.WINDOW_WIDTH - start_x_y[0]
            start_x_y[0] = offset + constants.WINDOW_WIDTH - self.radius
            vectors[0] = -vectors[0]
        return start_x_y, vectors


class Window:
    def __init__(self, width, height, title="PYVITY"):
        self.dimensions = (width, height)
        self.title = title


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    