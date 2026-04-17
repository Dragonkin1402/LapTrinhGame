import pygame

def draw_menu(screen):
    screen.fill((0,0,0))

    font = pygame.font.Font(None, 80)
    title = font.render("KIEM HIEP GAME", True, (255,255,255))
    screen.blit(title, (200,200))

    font2 = pygame.font.Font(None, 40)
    start = font2.render("Press SPACE to Start", True, (200,200,200))
    screen.blit(start, (250,350))