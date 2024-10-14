# Example file showing a basic pygame "game loop"
import pygame
import random
import time
import threading
import math

import pygame.sysfont

# pygame setup
pygame.init()
Screen_W = 1280
Screen_H = 720
screen = pygame.display.set_mode((Screen_W, Screen_H))
clock = pygame.time.Clock()
running = True
dt = 0
## game para
score = 0
fontSize = 40
Font = pygame.font.Font("fonts\\joystix.ttf",fontSize)
lifes = 1


player_size = math.floor((Screen_W / 21,33333333)[0])# * 2 #60
player_pos = pygame.Vector2(Screen_W / 2, Screen_H - player_size)
base_player_speed = 300  # Base player speed

showHitboxes = False #enable hitbox debugging

player_image = pygame.image.load("Sprites\\player.png")
player_image = pygame.transform.scale(player_image, (player_size,player_size))
player_colision = pygame.Rect(0,0, player_size,player_size)

# Variables to handle increasing speed
speed_multiplier = 1.5  # Multiplier for increasing speed over time
time_held_a = 0  # Time the 'A' key has been held down
time_held_d = 0  # Time the 'D' key has been held down
increase_rate = 1  # How quickly the speed increases per second

BaseFallSpeedMult = 1 #2

enemies = []  # Store enemies here
enemy_size = round(Screen_W / 32)# * 2 #40
enemy_image = pygame.image.load("Sprites\\angry.png") 
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

bg_image = pygame.image.load("Sprites\\background.png")
bg_image = pygame.transform.scale(bg_image,(Screen_W,Screen_H))

#Sounds
## MUSIC ##
pygame.mixer.music.load(r"audio\\bg_music.mp3")
pygame.mixer.music.play(-1,0,0)
## SOUNDS ##
lostLife = pygame.mixer.Sound("audio\\hit.mp3")
killEnemy = pygame.mixer.Sound("audio\\kill.wav")
##############################################


startTime = time.time()
#on start reset this ^


def spawnEnemy():
    """Spawns enemies at random intervals"""
    while running:
        EnemyPos = pygame.Vector2(random.randint(enemy_size, Screen_W - enemy_size), 0)
        enemies.append([enemy_image, EnemyPos, pygame.Rect(EnemyPos.x,EnemyPos.y,enemy_size,enemy_size),time.time()])  # Append enemy with size, position, and speed
        time.sleep(random.randint(2, 3))  # Delay between spawning
        

# Start the enemy spawning thread
spawnThread = threading.Thread(target=spawnEnemy)
spawnThread.start()


#Text rendering funtion
def drawText(i,col,pos,font,render):
    img = font.render(i,True,col) # text, ,color
    img_rect = img.get_rect()
    img_rect.topright = pygame.Vector2(Screen_W, pos)
    
    #print(img_rect)
    if render:
        screen.blit(img,(img_rect))
    else:
        return img_rect
    


while running:
    timePlayed = time.time()-startTime
    if timePlayed <= 100:
        if pygame.key.get_pressed()[pygame.K_s]:
            BaseFallSpeedMult = 2 + timePlayed / 100
        else:
            BaseFallSpeedMult = 1 + timePlayed / 100

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightblue")
    #render image
    screen.blit(bg_image,(0,0))
    #pygame.draw.circle(screen,"red",player_pos,player_size) # Draws Player, in this case a Circle.a
    
    screen.blit(player_image, (player_pos.x,player_pos.y))
    player_colision.topleft = player_pos

    def TestEnemy(enemy):
        #if time.time() - enemy[3] >= (3.5 * (Screen_H / 720)): # times it lol im dumb
        if enemy[1].y >= Screen_H:
            enemies.remove(enemy)
          #  print("LOST A LEVEL")
            pygame.mixer.Sound.play(lostLife)
            #if lifes - 1 <= 0:
                # handle game over

    for enemy in enemies:
        enemy[1].y += 200 * dt * BaseFallSpeedMult # * timer / 150 # Move enemy downward
        screen.blit(enemy[0], (enemy[1].x, enemy[1].y))
        threading.Thread(target=TestEnemy, args=[enemy]).start()


    # Collision
        for enemy in enemies:
            enemy[2].topleft = enemy[1]
            if player_colision.colliderect(enemy[2]):
               # print("COLLISION!!!!!!!!!!!!")
                enemies.remove(enemy)
                pygame.mixer.Sound.play(killEnemy)
                score += 1
                
    if showHitboxes: 
        pygame.draw.rect(screen,"Red",player_colision)
    for enemy in enemies:
        if showHitboxes:
            pygame.draw.rect(screen,"Green",enemy[2])


        
    
    keys = pygame.key.get_pressed()

    # Increase speed over time if A or D is held
    if keys[pygame.K_s]:
        BaseFallSpeedMult = 2
    else:
        BaseFallSpeedMult = 1

    if keys[pygame.K_a]:
        time_held_a += dt  # Track how long A is held
        speed_multiplier = 1.0 + increase_rate * time_held_a  # Speed increases with time
        if player_pos.x >= 1:
            player_pos.x -= base_player_speed * speed_multiplier * dt
    else:
        time_held_a = 0  # Reset if key is released

    if keys[pygame.K_d]:
        time_held_d += dt  # Track how long D is held
        speed_multiplier = 1.0 + increase_rate * time_held_d  # Speed increases with time
        if player_pos.x <= (Screen_W - player_size):
            player_pos.x += base_player_speed * speed_multiplier * dt
    else:
        time_held_d = 0  # Reset if key is released

    # flip() the display to put your work on screen
    #render score
    drawText("Score " + str(score),(0,0,0),(0),Font,True) #score, position(x,y),font(font,size)
    #render time
    drawText("Time " + str(round(timePlayed)),(0,0,0), (-10 +  drawText("1","red",0,Font,False).height ),Font,True) #time, col, (top right corner -  (score + y padding)),font
    # only for text debugging purposes ! pygame.draw.rect(screen,"orange",drawText("text","black",(0,0),Font))
    pygame.display.flip()

   

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

spawnThread.join()

pygame.quit()