import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - Final Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (5, 5, 15)
RED = (255, 60, 60)
GREEN = (0, 220, 120)
BLUE = (80, 160, 255)
YELLOW = (255, 230, 80)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28, bold=True)
big_font = pygame.font.SysFont("Arial", 42, bold=True)

# Player ship
player_width = 60
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 6

# Bullets (bigger size)
bullet_width = 8
bullet_height = 20
bullet_speed = 9
bullets = []

# Enemies
enemy_width = 50
enemy_height = 30
enemy_speed = 1.2   # slow start
enemy_count = 6
enemies = []

# Score and lives
score = 0          # increases per bullet fired
lives = 5          # game over after 5 touches


def create_enemies():
    global enemies
    enemies = []
    for _ in range(enemy_count):
        x = random.randint(0, WIDTH - enemy_width)
        y = random.randint(-400, -40)
        enemies.append([x, y])


def reset_game():
    global player_x, bullets, score, lives, enemy_speed
    player_x = WIDTH // 2 - player_width // 2
    bullets = []
    score = 0
    lives = 5
    enemy_speed = 1.2
    create_enemies()


def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, YELLOW, (player_x + player_width//2 - 5, player_y - 8, 10, 8))


def draw_bullets():
    for b in bullets:
        pygame.draw.rect(screen, GREEN, (b[0], b[1], bullet_width, bullet_height))


def draw_enemies():
    for e in enemies:
        pygame.draw.rect(screen, RED, (e[0], e[1], enemy_width, enemy_height))
        pygame.draw.rect(screen, YELLOW, (e[0] + 10, e[1] + 8, 10, 5))


def game_over_screen():
    while True:
        screen.fill(BLACK)

        over = big_font.render("GAME OVER!", True, RED)
        score_text = font.render(f"Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart", True, BLUE)
        exit_text = font.render("Press ESC to Exit", True, YELLOW)

        screen.blit(over, (WIDTH//2 - over.get_width()//2, 190))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 240))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 300))
        screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, 340))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Start enemies
create_enemies()

# =========================
#        MAIN LOOP
# =========================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Shooting adds score
            if event.key == pygame.K_SPACE:
                score += 1
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y - bullet_height
                bullets.append([bullet_x, bullet_y])

    # Movement
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
        player_x -= player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width:
        player_x += player_speed

    # Move bullets
    for b in bullets:
        b[1] -= bullet_speed
    bullets = [b for b in bullets if b[1] + bullet_height > 0]

    # Slowly increase enemy speed
    enemy_speed += 0.0006

    # Move enemies and respawn if bottom reached (NO life loss)
    for e in enemies[:]:
        e[1] += enemy_speed
        if e[1] > HEIGHT:
            enemies.remove(e)
            enemies.append([random.randint(0, WIDTH - enemy_width), random.randint(-400, -40)])

    # Bullet hits enemy → enemy disappears
    for b in bullets[:]:
        bx, by = b
        for e in enemies[:]:
            ex, ey = e
            if (bx < ex + enemy_width and
                bx + bullet_width > ex and
                by < ey + enemy_height and
                by + bullet_height > ey):
                bullets.remove(b)
                enemies.remove(e)
                enemies.append([random.randint(0, WIDTH - enemy_width), random.randint(-400, -40)])
                break

    # Player collision → lose life
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for e in enemies[:]:
        enemy_rect = pygame.Rect(e[0], e[1], enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            enemies.remove(e)
            enemies.append([random.randint(0, WIDTH - enemy_width), random.randint(-400, -40)])

    # Game over after 5 touches
    if lives <= 0:
        game_over_screen()

    # Draw
    screen.fill(BLACK)

    # Stars background
    for _ in range(20):
        pygame.draw.circle(screen, WHITE, (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 1)

    draw_player()
    draw_bullets()
    draw_enemies()

    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    pygame.display.update()
    clock.tick(60)
