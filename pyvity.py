import pygame
import math

from settings import Ball, Window, Background
import constants

def setup():
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    window = Window(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, "PYVITY")
    screen = pygame.display.set_mode(window.dimensions)
    pygame.display.set_caption(window.title)
    radius = constants.BALL_RADIUS
    ball = Ball(color=(255, 244, 125), center=(window.dimensions[0] / 2, window.dimensions[1] - radius), radius=radius)
    return screen, ball, my_font


def render_window(screen, bg, ball, line, shoot, text):
    screen.fill((64, 64, 64))
    screen.blit(bg.image, bg.rect)
    screen.blit(text, (0, 0))
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


def in_motion(ball, start_x_y, vectors, percentage_power, time, current_planet):
    if ball.center[1] <= constants.WINDOW_HEIGHT - ball.radius:
        start_x_y, vectors = ball.check_boundaries(start_x_y, vectors)
        ball.center = ball.ball_path(start_x_y, vectors, time, constants.PLANETS[current_planet]["gravity"])
        return True, start_x_y, time, vectors
    else:
        vectors = [vector * percentage_power for vector in vectors] 
        time = 0
        ball.center = (ball.center[0], constants.WINDOW_HEIGHT - ball.radius)
        start_x_y = [ball.center[0], ball.center[1]]
        if get_magnitude(vectors) <= 0.1:
            ball.center = (ball.center[0], constants.WINDOW_HEIGHT - ball.radius)
            return False, start_x_y, time, vectors
        return True, start_x_y, time, vectors
        

def get_events(running, shoot, time, start_x_y, ball, current_planet):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and shoot == False:
            time = 0
            shoot = True
            start_x_y = [ball.center[0], ball.center[1]]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_planet -= 1
                if current_planet < 0:
                    current_planet = len(constants.PLANETS) - 1
            elif event.key == pygame.K_RIGHT:
                current_planet += 1
                if current_planet >= len(constants.PLANETS):
                    current_planet = 0
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    img = constants.PLANETS[current_planet]["bg"]
    bg = Background(f"./backgrounds/{img}", [0, 0])

    return running, time, shoot, start_x_y, bg, current_planet


def run(screen, ball, my_font):
    running = True
    shoot = False
    time = 0
    percentage_power = 0.66
    start_x_y = [0, 0]
    current_planet = 2
    while running:

        if shoot:
            shoot, start_x_y, time, vectors = in_motion(ball, start_x_y, vectors, percentage_power, time, current_planet)
            time += 0.1
        
        else:
            vectors = get_vectors(pygame.mouse.get_pos(), ball.center)
            line = [ball.center, vectors]
        
        running, time, shoot, start_x_y, bg, current_planet = get_events(running, shoot, time, start_x_y, ball, current_planet)
        text = my_font.render(constants.PLANETS[current_planet]["title"], False, (255, 255, 255))
        render_window(screen, bg, ball, line, shoot, text)


def main():
    screen, ball, my_font = setup()
    run(screen, ball, my_font)
    pygame.quit()


if __name__ == "__main__":
    main()
