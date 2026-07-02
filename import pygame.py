import pygame
import random
import math
import sys

pygame.init()

# =========================
# Screen
# =========================
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thunder Strike PRO")

clock = pygame.time.Clock()

# =========================
# Colors
# =========================
WHITE = (255,255,255)
RED = (255,60,60)
GREEN = (0,255,120)
BLUE = (80,160,255)
BLACK = (10,10,20)
YELLOW = (255,230,0)

# =========================
# Sounds (optional fallback safe)
# =========================
shoot_sound = None
boom_sound = None

# =========================
# Fonts
# =========================
font = pygame.font.SysFont("consolas", 22)
big_font = pygame.font.SysFont("consolas", 48)

# =========================
# Player
# =========================
player = pygame.Rect(230, 600, 40, 40)
player_speed = 6
hp = 5

# =========================
# Game objects
# =========================
bullets = []
enemies = []
boss = None

score = 0
level = 1

weapon_mode = 1  # 1 normal, 2 spread

# =========================
# Background scroll
# =========================
bg_y = 0

# =========================
# States
# =========================
MENU = 0
PLAYING = 1
GAMEOVER = 2

state = MENU

# =========================
# Functions
# =========================
def draw_text(text, x, y, color=WHITE, f=font):
    screen.blit(f.render(text, True, color), (x,y))

def spawn_enemy():
    x = random.randint(20, WIDTH-60)
    enemies.append(pygame.Rect(x, -40, 40, 40))

def spawn_boss():
    return {
        "rect": pygame.Rect(150, -150, 200, 120),
        "hp": 30
    }

# =========================
# Game Loop
# =========================
running = True
enemy_timer = 0

while running:
    clock.tick(60)

    # =========================
    # Events
    # =========================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if state == MENU:
                if event.key == pygame.K_SPACE:
                    state = PLAYING

            elif state == PLAYING:
                if event.key == pygame.K_z:
                    weapon_mode = 1
                if event.key == pygame.K_x:
                    weapon_mode = 2

            elif state == GAMEOVER:
                if event.key == pygame.K_SPACE:
                    # reset
                    hp = 5
                    score = 0
                    level = 1
                    enemies.clear()
                    bullets.clear()
                    boss = None
                    player.x = 230
                    state = MENU

    keys = pygame.key.get_pressed()

    # =========================
    # MENU
    # =========================
    if state == MENU:
        screen.fill(BLACK)
        draw_text("THUNDER STRIKE PRO", 80, 200, YELLOW, big_font)
        draw_text("Press SPACE to Start", 130, 300)
        pygame.display.update()
        continue

    # =========================
    # GAME OVER
    # =========================
    if state == GAMEOVER:
        screen.fill(BLACK)
        draw_text("GAME OVER", 170, 250, RED, big_font)
        draw_text(f"Score: {score}", 200, 330)
        draw_text("Press SPACE", 180, 380)
        pygame.display.update()
        continue

    # =========================
    # PLAYER MOVE
    # =========================
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    player.x = max(0, min(WIDTH-40, player.x))

    # =========================
    # SHOOT
    # =========================
    if keys[pygame.K_SPACE]:
        if len(bullets) < 10:

            if weapon_mode == 1:
                bullets.append(pygame.Rect(player.centerx, player.y, 5, 10))

            elif weapon_mode == 2:
                bullets.append(pygame.Rect(player.centerx-10, player.y, 5, 10))
                bullets.append(pygame.Rect(player.centerx, player.y, 5, 10))
                bullets.append(pygame.Rect(player.centerx+10, player.y, 5, 10))

    # =========================
    # Background scroll
    # =========================
    bg_y += 2
    if bg_y > HEIGHT:
        bg_y = 0

    screen.fill(BLACK)

    # =========================
    # LEVEL SYSTEM
    # =========================
    if score > level * 10:
        level += 1
        if level % 3 == 0 and boss is None:
            boss = spawn_boss()

    # =========================
    # ENEMY SPAWN
    # =========================
    enemy_timer += 1
    if enemy_timer > max(20, 60 - level*5):
        spawn_enemy()
        enemy_timer = 0

    # =========================
    # UPDATE BULLETS
    # =========================
    for b in bullets[:]:
        b.y -= 10
        if b.y < 0:
            bullets.remove(b)

    # =========================
    # UPDATE ENEMIES
    # =========================
    for e in enemies[:]:
        e.y += 3 + level

        if e.colliderect(player):
            hp -= 1
            enemies.remove(e)
            if hp <= 0:
                state = GAMEOVER

        if e.y > HEIGHT:
            enemies.remove(e)
            hp -= 1
            if hp <= 0:
                state = GAMEOVER

    # =========================
    # BULLET HIT ENEMY
    # =========================
    for b in bullets[:]:
        for e in enemies[:]:
            if b.colliderect(e):
                try:
                    bullets.remove(b)
                    enemies.remove(e)
                    score += 1
                except:
                    pass

    # =========================
    # BOSS
    # =========================
    if boss:
        boss["rect"].y += 1

        if boss["rect"].y > 50:
            boss["rect"].y = 50

        # bullet hit boss
        for b in bullets[:]:
            if boss["rect"].colliderect(b):
                bullets.remove(b)
                boss["hp"] -= 1
                score += 2

        if boss["hp"] <= 0:
            boss = None
            score += 50

        pygame.draw.rect(screen, RED, boss["rect"])
        draw_text(f"BOSS HP: {boss['hp']}", 150, 10, RED)

    # =========================
    # DRAW PLAYER
    # =========================
    pygame.draw.rect(screen, BLUE, player)

    # =========================
    # DRAW BULLETS
    # =========================
    for b in bullets:
        pygame.draw.rect(screen, WHITE, b)

    # =========================
    # DRAW ENEMIES
    # =========================
    for e in enemies:
        pygame.draw.rect(screen, RED, e)

    # =========================
    # HP BAR
    # =========================
    pygame.draw.rect(screen, RED, (10, 650, 100, 10))
    pygame.draw.rect(screen, GREEN, (10, 650, hp * 20, 10))

    # =========================
    # UI
    # =========================
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Level: {level}", 10, 35)
    draw_text(f"Weapon: {weapon_mode}", 10, 60)

    pygame.display.update()

pygame.quit()
sys.exit()   