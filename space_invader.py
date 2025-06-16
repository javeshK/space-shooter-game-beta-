import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("background.png")

#  Background sound
mixer.music.load("LAST LETTER.mp3")
mixer.music.play(-1)

# Title of game
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("spaceship (1).png")
pygame.display.set_icon(icon)

# Game over  text
over_font = pygame.font.Font("KILOTON1.TTF", 64)

# PLayer
playerimg = pygame.image.load("shooting_spaceship.png")
playerX = 360
playerY = 520
playerX_change = 0

# comet
cometimg = [] 
cometX = []
cometY = []
cometXchange = []
cometYchange = []
num_of_comets = 20
# loop for more comets
for i in range(num_of_comets):
    cometimg.append(pygame.image.load("comet.png"))
    cometX.append(random.randint(0,735))
    cometY.append(random.randint(50,100))
    cometXchange.append(1)
    cometYchange.append(40)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = 2
bullet_state = "ready" 
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving

# score
score_value = 0
font = pygame.font.Font("KILOTON1.TTF", 32)

textX = 10
textY = 10

# SCORE     
def show_score(x,y):
    score = font.render("Score :"+ str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

# Game over
def game_over_text(x,y):
    over = over_font.render("Game Over ", True, (255,255,255))
    screen.blit(over, (x,y))

def player(x,y):
    screen.blit(playerimg,(x, y))  #.blit() means to draw(has 2 paramerts(img, (x,ycoordinates)))
# comet appearence (blit)
def comet(x,y,i):
    screen.blit(cometimg[i],(x, y))
# fire function
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x +16, y +10))
#  collision
def isCollision(cometX, cometY, bulletX, bulletY):
    distance = math.sqrt((math.pow(cometX - bulletX, 2)) + (math.pow(cometY-bulletY, 2)))
    if distance < 22:
        return True
    else:
        return False

# Game Loop 
running = True
while running:
    # RGB = red, green, blue
    screen.fill((240,200,240))
    # background image
    screen.blit(background,(0,0))
    # for exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #  if keystroke is pressed  whetther its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_RCTRL:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav") 
                    bullet_sound.play() 
                    # get the current coordinate of the spaceship  
                    bulletX = playerX 
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                

    # shooter appearance
    playerX += playerX_change
    # Booundry check for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # comet appearance
    for i in range(num_of_comets):
        # Game Over
        if cometY[i] > 460:
            for j in range(num_of_comets):
                cometY[j] = 2000
            game_over_text(150,250)        
            
        cometX[i] += cometXchange[i]
        # movement of comet
        if cometX[i] <= 0:
            cometXchange[i] = 0.3
            cometY[i] += cometYchange[i]
        elif cometX[i] >= 768:
            cometXchange[i] = -0.3
            cometY[i] += cometYchange[i]
        #  collision
        collision = isCollision(cometX[i],cometY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY= 480
            bullet_state = "ready"
            score_value += 1
            cometX[i] = random.randint(0,735)
            cometY[i] = random.randint(50,100)
        comet(cometX[i],cometY[i], i)
    
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange

    player(playerX,playerY)
    show_score(textX, textY)
    
    pygame.display.update()

    