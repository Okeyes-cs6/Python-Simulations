import pygame
import math


pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

# Radii Setup
RADII = [105, 23, 40, 43, 27]
SCALED_RADII = [radius / (RADII[0] / 30) for radius in RADII]

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
RED = (188, 39, 50)
BLUE = (100, 149, 237)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)

# Font
FONT = pygame.font.SysFont("comicsans", 16)
COUNTER_FONT = pygame.font.SysFont("comicsans", 25)

class PlanetaryBody:
    AU = 146.6e6 * 1000 # astronomical unit in meters
    G = 6.67428e-11 # gravitational constant
    SCALE = 250 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # how much time elapsed (1 day in s)

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius # meters
        self.color = color
        self.mass = mass # kilograms

        self.orbit = [] # keeps track of all the points for the planet
        self.sun = False # keeps sun from orbiting
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []

            for point in self.orbit:
                point_x, point_y = point
                point_x = point_x * self.SCALE + WIDTH / 2
                point_y = point_y * self.SCALE + HEIGHT / 2

                updated_points.append((point_x, point_y))

            pygame.draw.lines(window, self.color, False, updated_points, 1)

        pygame.draw.circle(window, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)} km", 1, WHITE)
            WINDOW.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y

        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planetary_bodies):
        total_fx = total_fy = 0
        for body in planetary_bodies:
            if self == body:
                continue

            fx, fy = self.attraction(body)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))


def main():
    running = True
    clock = pygame.time.Clock()

    sun = PlanetaryBody(0, 0, SCALED_RADII[0], YELLOW, 1.98892e30)
    sun.sun = True

    mercury = PlanetaryBody(0.387 * PlanetaryBody.AU, 0, SCALED_RADII[1], DARK_GREY, 3.30e23)
    mercury.y_vel = -47.4 * 1000

    venus = PlanetaryBody(0.723 * PlanetaryBody.AU, 0, SCALED_RADII[2], ORANGE, 4.8685e24)
    venus.y_vel = -35.02 * 1000

    earth = PlanetaryBody(-1 * PlanetaryBody.AU, 0, SCALED_RADII[3], BLUE, 5.9742e24)
    earth.y_vel = 29.783 * 1000

    mars = PlanetaryBody(-1.524 * PlanetaryBody.AU, 0, SCALED_RADII[4], RED, 6.39e23)
    mars.y_vel = 24.077 * 1000

    planetary_bodies = [sun, mercury, venus, earth, mars]

    while running:
        clock.tick(60) # regulates number of frame rates (max)
        WINDOW.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for body in planetary_bodies:
            body.update_position(planetary_bodies)
            body.draw(WINDOW)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()