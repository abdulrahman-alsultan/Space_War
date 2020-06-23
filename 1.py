import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('First game')
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

background = pygame.image.load("1083.jpg")

playerImage = pygame.image.load("space-invader.png")
Px = 370
Py = 480
PChangeX = 0
PChangeY = 0

enemyImage = pygame.image.load("space-invaders.png")
Ex = random.randint(0, 730)
Ey = 40
numOfEnemy = 6


bullets = pygame.image.load("bullet.png")
Bx = Px
By = Py
boolean = False

score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

GameOver = pygame.font.Font("freesansbold.ttf", 64)
GO = False


def Show_score():
    s = font.render("score: " + str(score), True, (255, 255, 255))
    screen.blit(s, (10, 10))


def player(x, y):
    screen.blit(playerImage, (round(x), round(y)))


def enemy(x, y):
    screen.blit(enemyImage, (round(x), round(y)))


def BulletsShooting(x, y):
    screen.blit(bullets, (round(x), round(y)))


def isColl(ex, ey, bx, by):
    dis = math.sqrt(math.pow(ex - bx, 2) + math.pow(ey - by, 2))
    if dis < 50:
        return True
    return False


def crash(px, py, ex, ey):
    global Ex, Ey, GO
    if (Px - Ex) < 10 and Ey+64 == Py:
        Ey = 2000
        Ex = 2000
        g = GameOver.render("GAME OVER ", True, (0, 0, 0))
        screen.blit(g, (200, 300))
        GO = True


while True:
    # hex to RGB color
    screen.fill((128, 128, 128))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PChangeX = -2
            if event.key == pygame.K_RIGHT:
                PChangeX = 2
            if event.key == pygame.K_UP:
                PChangeY = -2
            if event.key == pygame.K_DOWN:
                PChangeY = 2
            if event.key == pygame.K_SPACE:
                boolean = True
                sound_of_bullet = mixer.Sound("laser.wav")
                sound_of_bullet.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                PChangeX = 0
                PChangeY = 0
    if PChangeY > 0:
        if Py < 530:
            Py += PChangeY
    elif PChangeY < 0:
        if Py > 300:
            Py += PChangeY

    if PChangeX > 0:
        if Px < 730:
            Px += PChangeX
    elif PChangeX < 0:
        if Px > 0:
            Px += PChangeX

    Ey += 1
    if boolean:
        BulletsShooting(Bx, By)
        By -= 2
    else:
        Bx = Px
        By = Py
    if By < 0:
        boolean = False
        Bx = Px
        By = Py

    if isColl(Ex, Ey, Bx, By) and boolean:
        mixer.Sound("explosion.wav").play()
        boolean = False
        score += 1
        Bx = Px
        By = Py
        Ex = random.randint(0, 730)
        Ey = 40

    player(Px, Py)
    enemy(Ex, Ey)
    Show_score()
    if Ey > 600:
        if GO:
            g = GameOver.render("GAME OVER ", True, (0, 0, 0))
            screen.blit(g, (200, 300))
        else:
            Ex = random.randint(0, 730)
            Ey = 40
            enemy(Ex, Ey)

    crash(Px, Py, Ex, Ey)

    pygame.display.update()
