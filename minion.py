import pygame
import random

class Minion:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.hp = 2

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        self.x += dx * 0.02
        self.y += dy * 0.02

    def draw(self, screen):
        pygame.draw.circle(screen, (255,150,0), (int(self.x), int(self.y)), 15)

    def take_damage(self, dmg):
        self.hp -= dmg