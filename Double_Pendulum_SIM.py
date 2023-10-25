import pygame
from pygame.locals import *
from math import sin, cos, pi, sqrt

# GLOBAL VARIABLES

m1, m2 = 40, 40  # Mass of the pendulum
ang1, ang2 = pi / 2, pi / 8
leng1, leng2 = 200, 200
window_size = (1280, 720)
verts = (window_size[0] / 2, 250)
initial_point = (0, 0)
trace = []
trace_size = 1000
framesbt = 1
counter = 0
gravity = 2
air_resistance = 1
FPS = 45

# CLASSES


class Pendulum:

    def __init__(self, vertices, mass, length, angle):
        self.vertice = vertices
        self.mass = mass
        self.length = length
        self.angle = angle
        self.vel = 0
        self.aceleration = 0
        self.pos_x = (sin(self.angle) * self.length) + self.vertice[0]
        self.pos_y = (cos(self.angle) * self.length) + self.vertice[1]
        self.final_position = (self.pos_x, self.pos_y)

    def get_position(self):
        self.pos_x = (sin(self.angle) * self.length) + self.vertice[0]
        self.pos_y = (cos(self.angle) * self.length) + self.vertice[1]
        self.final_position = (self.pos_x, self.pos_y)
        return self.final_position

    def update(self, penumb):

        ot_vel, ot_ang, ot_mass, ot_len = penumb[1], penumb[2], penumb[3], penumb[4]

        if penumb[0]:
            func1 = -gravity * (2 * self.mass + ot_mass) * sin(self.angle)
            func2 = -ot_mass * gravity * sin(self.angle - 2 * ot_ang)
            func3 = -2 * sin(self.angle - ot_ang) * ot_mass
            func4 = ot_vel * ot_vel * ot_len + self.vel * self.vel * self.length * cos(self.angle - ot_ang)
            den = self.length * (2 * self.mass + ot_mass - ot_mass * cos(2 * self.angle - 2 * ot_ang))
            self.aceleration = (func1 + func2 + func3 * func4) / den
        else:
            func1 = 2 * sin(ot_ang - self.angle)
            func2 = (ot_vel * ot_vel * ot_len * (ot_mass + self.mass))
            func3 = gravity * (ot_mass + self.mass) * cos(ot_ang)
            func4 = self.vel * self.vel * self.length * self.mass * cos(ot_ang - self.angle)
            den = self.length * (2 * ot_mass + self.mass - self.mass * cos(2 * ot_ang - 2 * self.angle))
            self.aceleration = (func1 * (func2 + func3 + func4)) / den

        self.vel += self.aceleration
        self.angle += self.vel
        self.vel *= air_resistance

    def draw(self, surface):
        pygame.draw.line(surface, 'black', self.vertice, self.final_position, width=4)
        pygame.draw.circle(surface, 'black', self.final_position, self.mass / 2)


def distance_b2p(point_a, point_b):
    dis_a = (round(point_a[1]) - round(point_a[0])) * (round(point_a[1]) - round(point_a[0]))
    dis_b = (round(point_b[1]) - round(point_b[0])) * (round(point_b[1]) - round(point_b[0]))
    distances = sqrt((dis_a + dis_b))
    print(distances)
    return distances


if __name__ == '__main__':

    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Double Pendulum")
    pendulum_1 = Pendulum(verts, m1, leng1, ang1)
    pendulum_2 = Pendulum(verts, m2, leng2, ang2)
    radius_p2 = pendulum_2.mass
    clock = pygame.time.Clock()
    mouse_clicked = False

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                pend_xy = pendulum_2.final_position
                distance = distance_b2p(mouse_xy, pend_xy)
                if distance <= radius_p2:
                    mouse_clicked = True

            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = False

        pygame.draw.rect(window, 'white', initial_point + window_size)

        if not mouse_clicked:
            pendulum_1.get_position()
            pendulum_2.vertice = pendulum_1.final_position
            pendulum_2.get_position()
            infopen1 = [True, pendulum_2.vel, pendulum_2.angle, pendulum_2.mass, pendulum_2.length]
            infopen2 = [False, pendulum_1.vel, pendulum_1.angle, pendulum_1.mass, pendulum_1.length]
            pendulum_1.update(infopen1)
            pendulum_2.update(infopen2)

        else:
            mouse_xy = pygame.mouse.get_pos()
            pendulum_2.final_position = mouse_xy
            pendulum_2.length = distance_b2p(pendulum_2.vertice, pendulum_2.final_position)

        if counter >= framesbt:
            trace.append(pendulum_2.final_position)
            counter = 0

        if len(trace) >= 2:
            pygame.draw.lines(window, 'black', False, trace, width=4)
            if len(trace) >= trace_size:
                trace.pop(0)

        counter += 1
        pendulum_1.draw(window)
        pendulum_2.draw(window)
        pygame.display.update()
        clock.tick(FPS)
