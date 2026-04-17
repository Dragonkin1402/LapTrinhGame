import pygame
import random
import math
import os
from bullet import Bullet

class Enemy:
    def __init__(self):
        base = os.path.dirname(__file__)

        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)

        self.hp = 5
        self.max_hp = 5

        self.is_boss = False

        # 🎨 boss image
        try:
            self.boss_img = pygame.image.load(os.path.join(base, "assets/boss.png"))
            self.boss_img = pygame.transform.scale(self.boss_img, (120, 120))
        except:
            self.boss_img = None

    def update(self, speed):
        if self.is_boss:
            # 🔥 boss rung nhẹ
            self.x += random.randint(-2, 2)
            self.y += random.randint(-2, 2)
        else:
            self.x += random.choice([-1, 1]) * speed
            self.y += random.choice([-1, 1]) * speed

    def draw(self, screen):
        if self.is_boss and self.boss_img:
            screen.blit(self.boss_img, (self.x - 60, self.y - 60))

            # aura boss
            pygame.draw.circle(screen, (255,0,0), (int(self.x), int(self.y)), 70, 2)
        else:
            pygame.draw.circle(screen, (255,150,0), (int(self.x), int(self.y)), 20)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def boss_skill(self, player, bullets):
        # 💥 bắn vòng tròn
        if random.randint(0, 80) == 0:
            for angle in range(0, 360, 30):
                dx = math.cos(math.radians(angle))
                dy = math.sin(math.radians(angle))
                bullets.append(Bullet(self.x, self.y, dx, dy))

        # ⚡ dash vào player
        if random.randint(0, 120) == 0:
            dx = player.x - self.x
            dy = player.y - self.y

            self.x += dx * 0.2
            self.y += dy * 0.2