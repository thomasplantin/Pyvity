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
    def ball_path(start_x_y, vectors, time):
        velocity_x = vectors[0] * (1 - constants.PERCENTAGE_HANDICAP)
        velocity_y = vectors[1] * (1 - constants.PERCENTAGE_HANDICAP)
        dist_x = velocity_x * time
        dist_y = velocity_y * time + 0.5 * constants.GRAVITY * math.pow(time, 2)
        return (round(start_x_y[0] + dist_x), round(start_x_y[1] + dist_y))

    def get_current_height(self):
        return self.center[1]


class Window:
    def __init__(self, width, height, title="PYVITY"):
        self.dimensions = (width, height)
        self.title = title

    