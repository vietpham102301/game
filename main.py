import pygame
import os


pygame.init()
pygame.mixer.init()
pygame.font.init()

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
pygame.display.set_caption("First Game!")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
VEL = 5
BULLET_VEL = 15
MAX_BULLET = 3
FPS = 60
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2
BLACK = (0, 0, 0)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (55, 40)), 270)
#HUMAN = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'human.png')), (100, 140))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    red_health_text = HEALTH_FONT.render("health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)
    # WIN.blit(HUMAN, (human.x, human.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y +yellow.height +10 + VEL < HEIGHT:
        yellow.y += VEL
    if key_pressed[pygame.K_d] and yellow.x +yellow.width + VEL < BORDER.x:
        yellow.x += VEL


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, ((WIDTH/2 - draw_text.get_width()//2), HEIGHT/2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width :
        red.x -= VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y +red.height +10 + VEL < HEIGHT:
        red.y += VEL
    if key_pressed[pygame.K_RIGHT] and red.x +red.width + VEL < WIDTH +10:
        red.x += VEL


def handle_bullets(yellow_bullets, red_bullets, red, yellow, red_health, yellow_health):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # human = pygame.Rect(450, 250, 100, 140)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + red.height / 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "yellow win!"
        if yellow_health <= 0:
            winner_text = "red win!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        handle_bullets(yellow_bullets, red_bullets, red, yellow, red_health, yellow_health)
    main()


main()
