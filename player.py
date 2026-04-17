import pygame
import os
import time
import math
from effects import SlashEffect, ExplosionEffect

class Player:
    def __init__(self):
        base = os.path.dirname(__file__)

        self.frames = [
            pygame.image.load(os.path.join(base, "assets/player_idle.png")),
            pygame.image.load(os.path.join(base, "assets/player_attack.png"))
        ]
        self.frames = [pygame.transform.scale(f, (64,64)) for f in self.frames]

        self.frame_index = 0

        self.x = 400
        self.y = 300
        self.prev_pos = None

        self.trail = []
        self.max_trail = 10

        self.hp = 100
        self.max_hp = 100

        self.charge = 0
        self.last_skill_time = 0
        self.cooldown = 0.3

        self.effects = []

        # 🌳 skill tree
        self.skill_level = {
            "damage": 1,
            "charge": 1
        }

    def update(self, pos):
        if pos:
            dx = pos[0] - self.x
            dy = pos[1] - self.y

            # 🔥 giảm tốc độ (mượt hơn)
            self.x += dx * 0.08
            self.y += dy * 0.08

            self.trail.append((self.x, self.y))
            if len(self.trail) > self.max_trail:
                self.trail.pop(0)

            if self.prev_pos:
                speed = math.hypot(dx, dy)
                self.frame_index = 1 if speed > 20 else 0

            self.prev_pos = (self.x, self.y)

    def handle_skill(self, finger_count, enemy, minions):
        now = time.time()

        if now - self.last_skill_time < self.cooldown:
            return

        damage = self.skill_level["damage"]

        # 💀 giảm damage nếu là boss
        if enemy.is_boss:
            boss_multiplier = 0.3
        else:
            boss_multiplier = 1

        # ⚔️ chém 1
        if finger_count == 2:
            enemy.take_damage(1 * damage * boss_multiplier)

            for m in minions:
                if abs(self.x - m.x) < 50:
                    m.take_damage(1 * damage)

        # ⚔️ chém 3
        elif finger_count == 3:
            enemy.take_damage(3 * damage * boss_multiplier)

            for m in minions:
                if abs(self.x - m.x) < 70:
                    m.take_damage(2 * damage)

        # ⚡ tích lực
        elif finger_count == 0:
            self.charge += self.skill_level["charge"]

        # 💥 ulti
        elif finger_count == 5:
            if self.charge > 15:
                enemy.take_damage(10 * damage * boss_multiplier)

                for m in minions:
                    m.take_damage(5 * damage)

                self.effects.append(ExplosionEffect(self.x, self.y))
                self.charge = 0

        self.last_skill_time = now

    def draw(self, screen):
        # trail
        for i in range(len(self.trail)-1):
            alpha = int(255 * (i / len(self.trail)))
            pygame.draw.line(screen, (alpha, alpha, 255),
                             self.trail[i], self.trail[i+1], 5)

        # effects
        for e in self.effects[:]:
            e.update()
            e.draw(screen)
            if e.life <= 0:
                self.effects.remove(e)

        if len(self.effects) > 30:
            self.effects.pop(0)

        screen.blit(self.frames[self.frame_index], (self.x-32, self.y-32))