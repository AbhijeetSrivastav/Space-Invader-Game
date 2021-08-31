_author__ = "Abhijeet Srivastav"
__copyright__ = "2020 Abhijeet Srivastav"
__license__ = "Public Domain"
__version__ = "1.0"

# Importing moduless
import math
import random
import pygame
from pygame import mixer

pygame.init()  # Initializes the game engine

""" Setting the properties of the game window"""
screen = pygame.display.set_mode((800, 600))

win_icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(win_icon)
pygame.display.set_caption('Space Invader')

backround = pygame.image.load('background.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 play it in loop

ENEMY_SPEED = 2
PLAYER_SPEED = 3
BULLET_SPEED = 6
ENEMY_DENSITY = 6
SCORE = 0

# Loading player and its assets
player_img = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(cord_x, cord_y):
    """blitz method is used to draw something on the screen in this
     case called surface"""
    screen.blit(player_img, (cord_x, cord_y))


"""For single enemy
    enemy_img = pygame.image.load('alien.png')
    enemyX = random.randint(0, 736)
    enemyY = random.randint(50, 150)
    enemyX_change = ENEMY_SPEED
    enemyY_change = 40
"""

# Creating multiple enemies and loading assets
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(ENEMY_DENSITY):
    enemy_img.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(ENEMY_SPEED)
    enemyY_change.append(40)


def enemy(x_cord, y_cord, enemy_index):
    screen.blit(enemy_img[enemy_index], (x_cord, y_cord))


# Loading bullet and its assets
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = BULLET_SPEED
bullet_state = 'ready'  # ready mean cant see bullet and active means bullet can be seen(motion)


def FireBullet(cord_x, cord_y):
    global bullet_state
    bullet_state = 'active'
    screen.blit(bullet_img, (cord_x + 16, cord_y + 10))


def CollisionDetection(cord_x_enemy, cord_y_enemy, cord_x_bullet, cord_y_bullet):
    """Distance between two points P(x1, y1) and Q(x2, y2) is given by:
        d(P, Q) = √ [(x2 − x1)² + (y2 − y1)²] {Distance formula} """
    X_difference = math.pow(cord_x_enemy - cord_x_bullet, 2)
    Y_difference = math.pow(cord_y_enemy - cord_y_bullet, 2)
    distance = math.sqrt(X_difference + Y_difference)

    if distance < 27:
        return True
    else:
        return False


def ShowScore(cord_x, cord_y):
    score_value = SCORE
    font = pygame.font.Font('freesansbold.ttf', 32)
    score = font.render('SCORE:' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (cord_x, cord_y))


def GameOverAlert():
    over_font = pygame.font.Font('freesansbold.ttf', 32)
    over = over_font.render(f'GAME OVER !', True, (255, 255, 255))
    game_over = mixer.Sound('gameover.wav')
    game_over.play(-1)
    screen.blit(over, (250, 245))


"""Anything we want to run all the time the game runs we will make it in 
       while loop to make it run infinitely until game is running"""
running = True
while running:
    screen.fill((0, 0, 0))  # Fills the colour to screen
    screen.blit(backround, (0, 0))

    for event in pygame.event.get():
        """Checking for the event of the pressing of the close"""
        if event.type == pygame.QUIT:
            running = False

        """Checking for the event of the pressing of the arrow keys """
        if event.type == pygame.KEYDOWN:
            """ KEYDOWN denotes the event of the pressed key """
            if event.key == pygame.K_LEFT:
                playerX_change -= PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                playerX_change += PLAYER_SPEED
            """"
            If you want y axis control too
                    if event.key == pygame.K_UP:
                            playerY_change -= PLAYER_SPEED
                    if event.key == pygame.K_DOWN:
                            playerY_change += PLAYER_SPEED
            """

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    """Only allows shooting of the bullet when it is in ready position"""
                    """Giving the bullet a sound"""
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get current x coordinate of spaceship
                    bulletX = playerX

                    # Space bar pressing calls the bullet function
                    FireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            """KEYUP is the event of releasing the arrow key"""
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    """Updating the value of the player x change and player y change"""
    playerX += playerX_change
    playerY += playerY_change

    """Adding restricting boundary to the spaceship movement area"""
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    elif playerY >= 538:
        playerY = 538
    elif playerY <= 0:
        playerY = 0

    """Adding restricting boundary to the alien appearance area"""
    for enemy_index in range(ENEMY_DENSITY):
        """Game ending case is collision of alien with ship"""
        if enemyY[enemy_index] > 442:
            for j in range(ENEMY_DENSITY):
                enemyY[enemy_index] = 2000
                GameOverAlert()
                break
        """Updating the value of the enemy x change and enemy y change"""
        enemyX[enemy_index] += enemyX_change[enemy_index]

        if enemyX[enemy_index] <= 0:
            enemyX_change[enemy_index] = ENEMY_SPEED
            enemyY[enemy_index] += enemyY_change[enemy_index]
        elif enemyX[enemy_index] >= 736:
            enemyX_change[enemy_index] = -ENEMY_SPEED
            enemyY[enemy_index] += enemyY_change[enemy_index]

        """Collision checking"""
        collision = CollisionDetection(enemyX[enemy_index], enemyY[enemy_index], bulletX, bulletY)
        if collision:
            """Giving the explosion Sound"""
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            # Increase the score on collision
            SCORE = SCORE + 1
            # Now respawn the alien to new position
            enemyX[enemy_index] = random.randint(0, 736)
            enemyY[enemy_index] = random.randint(50, 150)
        else:
            pass
        enemy(enemyX[enemy_index], enemyY[enemy_index], enemy_index)
    """Adding restrictions on Bullet Movement"""
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'active':
        FireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    ShowScore(10, 10)

    pygame.display.update()  # Update the display  periodically
