import pygame

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx * 5
        self.dy = dy * 5
        self.life = 100

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), 6)