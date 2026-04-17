import pygame
import os
import random
import json
from settings import *
from hand_tracking import HandTracking
from player import Player
from enemy import Enemy
from bullet import Bullet
from minion import Minion
from levels import levels
from menu import draw_menu

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kiếm Hiệp Gesture Game")
clock = pygame.time.Clock()

# ================= SAVE =================
def save_game(level):
    with open("save.json", "w") as f:
        json.dump({"level": level}, f)

def load_game():
    try:
        with open("save.json", "r") as f:
            return json.load(f)["level"]
    except:
        return 0

# ================= INIT =================
hand = HandTracking()
player = Player()
enemy = Enemy()

bullets = []
minions = []

game_state = "menu"
level_index = load_game()

if level_index >= len(levels):
    level_index = 0   # reset về đầu
current_level = levels[level_index]

base = os.path.dirname(__file__)

bg = pygame.image.load(os.path.join(base, current_level["bg"])).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 40)
font_big = pygame.font.Font(None, 80)

shake = 0

# boss intro
boss_intro = False
intro_timer = 0

running = True

# ================= LOOP =================
while running:

    # ================= MENU =================
    if game_state == "menu":
        draw_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "game"

                if event.key == pygame.K_1:
                    player.skill_level["damage"] += 1
                if event.key == pygame.K_2:
                    player.skill_level["charge"] += 1

        pygame.display.update()
        continue

    # ================= BOSS INTRO =================
    if boss_intro:
        screen.fill((0,0,0))

        text = font_big.render("BOSS XUẤT HIỆN!", True, (255,0,0))
        screen.blit(text, (WIDTH//2 - 200, HEIGHT//2))

        intro_timer -= 1

        if intro_timer <= 0:
            boss_intro = False

        pygame.display.update()
        clock.tick(60)
        continue

    # ================= GAME =================
    offset_x = random.randint(-shake, shake)
    offset_y = random.randint(-shake, shake)

    screen.blit(bg, (offset_x, offset_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # HAND INPUT
    pos, fingers = hand.get_data()
    player.update(pos)

    before_hp = enemy.hp
    player.handle_skill(fingers, enemy, minions)

    if enemy.hp < before_hp:
        shake = 5

    # ================= ENEMY =================
    if "boss" in current_level:
        enemy.is_boss = True
        enemy.update(current_level["speed"])

        enemy.boss_skill(player, bullets)

        # bắn đạn
        if random.randint(0, 30) == 0:
            dx = player.x - enemy.x
            dy = player.y - enemy.y
            length = (dx**2 + dy**2) ** 0.5

            if length != 0:
                dx /= length
                dy /= length

            bullets.append(Bullet(enemy.x, enemy.y, dx, dy))

    else:
        enemy.update(current_level["speed"])

    # ================= MINION =================
    if random.randint(0, 40) == 0:
        minions.append(Minion())

    for m in minions[:]:
        m.update(player)
        m.draw(screen)

        if abs(m.x - player.x) < 20:
            player.hp -= 1

        if m.hp <= 0:
            minions.remove(m)

    if len(minions) > 15:
        minions.pop(0)

    # ================= BULLET =================
    for b in bullets[:]:
        b.update()
        b.draw(screen)

        if abs(b.x - player.x) < 20 and abs(b.y - player.y) < 20:
            player.hp -= 2
            bullets.remove(b)

        if b.life <= 0:
            bullets.remove(b)

    if len(bullets) > 40:
        bullets.pop(0)

    # ================= LEVEL =================
    if enemy.hp <= 0:
        level_index += 1
        save_game(level_index)

        if level_index >= len(levels):
            game_state = "win"
        else:
            current_level = levels[level_index]

            enemy = Enemy()

            # 💀 boss trâu hơn
            if "boss" in current_level:
                enemy.hp = current_level["enemy_hp"] * 3
                enemy.max_hp = current_level["enemy_hp"] * 3
                enemy.is_boss = True

                enemy.x = WIDTH // 2
                enemy.y = HEIGHT // 2

                boss_intro = True
                intro_timer = 120
            else:
                enemy.hp = current_level["enemy_hp"]
                enemy.max_hp = current_level["enemy_hp"]

            # load background mới
            bg = pygame.image.load(os.path.join(base, current_level["bg"])).convert()
            bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # boss chạm người
    if enemy.is_boss:
        if abs(player.x - enemy.x) < 60:
            player.hp -= 1

    # ================= DRAW =================
    enemy.draw(screen)
    player.draw(screen)

    # ================= UI =================
    # player HP
    pygame.draw.rect(screen, (50,50,50), (10,10,220,24))
    pygame.draw.rect(screen, (0,255,0), (10,10,220*(player.hp/player.max_hp),24))

    # boss HP
    pygame.draw.rect(screen, (50,50,50), (WIDTH-230,10,220,24))
    pygame.draw.rect(screen, (255,0,0), (WIDTH-230,10,220*(enemy.hp/enemy.max_hp),24))

    # charge
    pygame.draw.rect(screen, (0,0,255), (10,40,200*(player.charge/15),10))

    # tên màn
    text = font.render(current_level["name"], True, (255,255,255))
    screen.blit(text, (WIDTH//2 - 100, 20))

    # cảnh báo low HP
    if player.hp < 30:
        pygame.draw.rect(screen, (255,0,0), (0,0,WIDTH,HEIGHT), 3)

    pygame.display.update()

    if shake > 0:
        shake -= 1

    clock.tick(60)

    # ================= GAME OVER =================
    if player.hp <= 0:
        screen.fill((0,0,0))
        text = font_big.render("GAME OVER", True, (255,0,0))
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # ================= WIN =================
    if game_state == "win":
        screen.fill((0,0,0))
        text = font_big.render("YOU WIN!", True, (0,255,0))
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

# ================= CLEAN =================
hand.release()
pygame.quit()