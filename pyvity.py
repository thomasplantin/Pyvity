import pygame
import math

from settings import Ball, Window
import constants

def setup():
    pygame.init()
    window = Window(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, "PYVITY")
    screen = pygame.display.set_mode(window.dimensions)
    pygame.display.set_caption(window.title)
    ball = Ball(color=(255, 244, 125), center=(window.dimensions[0] / 2, window.dimensions[1] - 5), radius=5)

    return screen, ball

def render_window(screen, ball, line, shoot):
    screen.fill((64, 64, 64))
    ball.draw(screen)
    if not shoot:
        pygame.draw.line(screen, (255, 255, 255), line[0], (line[0][0] + line[1][0], line[0][1] + line[1][1]))
    pygame.display.update()

def get_vectors(mouse_coordinates, ball_coordinates):
    vector_x = mouse_coordinates[0] - ball_coordinates[0]
    vector_y = mouse_coordinates[1] - ball_coordinates[1]
    power = math.sqrt(math.pow(vector_x, 2) + math.pow(vector_y, 2))
    angle = math.asin(abs(vector_y / power))

    if power > constants.POWER_LIMIT:
        power = constants.POWER_LIMIT
        if vector_x < 0:
            vector_x = - power * math.cos(angle)
        else:
            vector_x = power * math.cos(angle)
        vector_y = - power * math.sin(angle)

    return [vector_x, vector_y]

def get_magnitude(vectors):
    return math.sqrt(math.pow(vectors[0], 2) + math.pow(vectors[1], 2))

def in_motion(ball, start_x_y, vectors, percentage_power, time):
    if ball.center[1] <= constants.WINDOW_HEIGHT - ball.radius:
        start_x_y, vectors = ball.check_boundaries(start_x_y, vectors)
        ball.center = ball.ball_path(start_x_y, vectors, time)
        return True, start_x_y, time, vectors
    else:
        vectors = [vector * percentage_power for vector in vectors] 
        time = 0
        ball.center = (ball.center[0], constants.WINDOW_HEIGHT - ball.radius)
        start_x_y = [ball.center[0], ball.center[1]]
        if get_magnitude(vectors) <= 0.005:
            ball.center = (ball.center[0], constants.WINDOW_HEIGHT - ball.radius)
            return False, start_x_y, time, vectors
        return True, start_x_y, time, vectors
        

def run(screen, ball):
    running = True
    shoot = False
    time = 0
    percentage_power = 0.66
    start_x_y = [0, 0]
    while running:

        if shoot:
            shoot, start_x_y, time, vectors = in_motion(ball, start_x_y, vectors, percentage_power, time)
            time += 0.1
        
        else:
            vectors = get_vectors(pygame.mouse.get_pos(), ball.center)
            line = [ball.center, vectors]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and shoot == False:
                time = 0
                shoot = True
                start_x_y = [ball.center[0], ball.center[1]]
        render_window(screen, ball, line, shoot)


def main():
    screen, ball = setup()
    run(screen, ball)
    pygame.quit()


if __name__ == "__main__":
    main()
