import pygame
import random
import math
from pygame import mixer


pygame.init()
num = 1
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans", 32)
screen = pygame.display.set_mode((800,600))
jogando = "sim"
######################FPS##################

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps,True,pygame.Color("coral"))
    screen.blit(fps_text, (770,0))
    return fps_text

######################SCORE##########

SCORE = 0
def update_score():
    score_render = font.render(f"Score: {SCORE}",True,(209, 26, 255))    
    screen.blit(score_render, (10,0))
    
###############game over ########################

game_over_font = pygame.font.SysFont("Arial Black", 64)

def game_over():
    global jogando
    game_over_render = game_over_font.render("BOBÃO PERDEU", True, (0,0,0))
    screen.blit(game_over_render, (136,200))
    jogando = "nao"

####restart¨¨¨¨¨¨¨¨¨¨¨¨

def restart():
    global jogando
    global SCORE
    jogando = "sim"
    SCORE =0
    for i in range(num_enemies):
        enemyX.clear()
        enemyY.clear()  
    create_enemies()  
    enemy(enemyX[i],enemyY[i])
    
    
    
#background

fundo = pygame.image.load("joseph.jpg")

#musica background

mixer.music.load("background.wav")
mixer.music.play(-1)

#################slaaaaaaaaaaa#########################
pygame.display.set_caption("bananas invasoras")
banana = pygame.image.load("banana.png")
pygame.display.set_icon(banana)

#############player###############
playerIMG = pygame.image.load("macaco.png")
playerX = 400
playerY = 500
playerX_change=0

def player(x,y):
    screen.blit(playerIMG,(x,y))

#BALA################

bulletIMG = pygame.image.load("girafa.png")
bulletX = 0
bulletY = 500
bulletX_change=0
bulletY_change= 10
bullet_state = "invisivel"

def fire(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16,y + 10))


#enemy###############
enemyIMG = []
enemyX =[]
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

def create_enemies():

    for i in range(num_enemies):

        enemyIMG.append(pygame.image.load("banana.png"))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(5)
        enemyY_change.append(35)

def enemy(x,y):
    screen.blit(enemyIMG[0], (x,y))
    
################COLISAOOOOOOOOOOOOOOOO""""""""""""""
def colliding (enemyX,enemyY,bulletX,bulletY):
 # D = raiz[ (y1-y)^2 + (x1-x)^2 ]
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+ math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else: False
    
    
#########looop###########################


running = True
while running:

    screen.blit(fundo, (0,0))
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -10
                
            if event.key == pygame.K_d:
                playerX_change = 10
                
            if event.key == pygame.K_SPACE and bullet_state == "invisivel": 
                bullet_sound = mixer.Sound("SHOT.wav")   
                bullet_sound.play()          
                bulletX = playerX
                fire(playerX,bulletY)  
            
            if event.key ==pygame.K_RETURN and jogando == "nao":
                restart()
            
        if event.type == pygame.KEYUP :
            if  event.key == pygame.K_a or  event.key == pygame.K_d:
                playerX_change = 0
        ######closeeeeeeeeee#############
        if event.type == pygame.QUIT:
            running = False
    
    #entidades
    player(playerX,playerY)
    create_enemies()   
    update_score()
    update_fps() 
    

        
    #movimentação amigo

    playerX += playerX_change

    if playerX <= 0: playerX = 0
    elif playerX >=736:playerX = 736

    #movimentação inimigo
    
    for i in range (num_enemies):
        
        enemy(enemyX[i],enemyY[i])

        
        #game over
        
        if enemyY[i] > 440:
            for j in range(num_enemies):
                
                enemyY[j] =2000
            game_over()
            break
            
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] >=768:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] <= 0: 
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
               
       #colisão
       
        collision = colliding(enemyX[i], enemyY[i], bulletX, bulletY) 
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "invisivel"
            SCORE += 1
            enemyX[i] = random.randint(65,735)
            enemyY[i] = random.randint(50,150)
    
    #movimentação bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "invisivel"
    
    if bullet_state == "fire":
        fire(bulletX,bulletY)
        bulletY -= bulletY_change
    
    
       
    pygame.display.update()
    clock.tick(60)