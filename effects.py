import pygame
import math

class SlashEffect:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y

        self.dx = dx * 10
        self.dy = dy * 10

        self.life = 20

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 200, 255), (int(self.x), int(self.y)), 8)


class ExplosionEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.life = 15

    def update(self):
        self.radius += 3
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 100, 0),
                           (int(self.x), int(self.y)), self.radius, 2)
                           