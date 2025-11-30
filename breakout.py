#-- librerie --
import pygame
import random
import time
pygame.init()
pygame.mixer.init()
#assets 
gameover = pygame.image.load("assets/img/gameover.png")

suono_rimbalzo = pygame.mixer.Sound("assets/sound/rimbalzo.wav")
suono_punto = pygame.mixer.Sound("assets/sound/punto.wav")
suono_win = pygame.mixer.Sound("assets/sound/win.wav")
suono_gameover = pygame.mixer.Sound("assets/sound/gameover.wav")

suono_rimbalzo.set_volume(0.2)
suono_punto.set_volume(0.2)
suono_win.set_volume(0.2)
suono_gameover.set_volume(0.2)
#-- costanti --
screen= pygame.display.set_mode((800, 600))
ball_r=10
base_w , base_h = 100,10 #100,10
base_vel = 0.5
FPS = 1005 #1005
font = pygame.font.Font(None, 74)
margine_x=47
margine_y=60
#-- inizializzazioni --
def inizializza():
    global vel_x, vel_y
    global ball_x, ball_y
    global base_x, base_y
    global point
    global mattoncini
    vel_x=random.uniform(-0.05,0.05)
    vel_y = 0.2 #0.2
    ball_x, ball_y = 400, 300
    base_x, base_y = 350, 580
    point=0
    mattoncino_w=113
    mattoncino_h=20
    mattoncini=[]
    gap = 5
    distanza_x = 47
    distanza_y = 60
    for i in range(4):
        for j in range(6):
            x=distanza_x + j * (mattoncino_w + gap)
            y=distanza_y + i * (mattoncino_h + gap)
            mattoncini.append(pygame.Rect(x, y, mattoncino_w, mattoncino_h))

inizializza()


#-- funzioni --
# - aggiorno lo schermo -
def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
# - disegno gli oggetti nello schermo - 
def disegna():
    pygame.draw.circle(screen, pygame.Color('black'), (ball_x, ball_y), ball_r)
    pygame.draw.rect(screen, pygame.Color('black'), (base_x, base_y, base_w, base_h))
    conta_punti = font.render(str(point), True, (pygame.Color('black')))
    screen.blit(conta_punti, (383.5,10))
    for mattoncino in mattoncini:
        pygame.draw.rect(screen, pygame.Color('blue'), mattoncino)
# - aggiorno le hitbox degli oggetti -
def aggiorna_hitbox():
    global ball_rect 
    global base_rect 
    ball_rect = pygame.Rect(ball_x - ball_r, ball_y - ball_r, ball_r * 2, ball_r * 2)
    base_rect = pygame.Rect(base_x, base_y, base_w, base_h)
# - calcola rimbalzo - 
def rimbalzo():
    global vel_x 
    global vel_y 
    global point
    max_vel_x = 0.2
    tolleranza = 10
    if ball_rect.bottom >= base_rect.top and ball_rect.bottom <= base_rect.top + tolleranza and ball_rect.centerx >= base_rect.left and ball_rect.centerx <= base_rect.right:
        centro_base = base_x + base_w / 2
        distanza = (ball_x - centro_base) / (base_w / 2)
        vel_x = distanza * max_vel_x
        vel_y = -vel_y
        suono_rimbalzo.play()

    
def stop():
    suono_gameover.play()
    screen.blit(gameover, (300,280))
    aggiorna()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    inizializza()
                    return
def win():
    suono_win.play()
    font_vittoria = pygame.font.SysFont("Times New Roman", 100)
    vittoria = font.render("Hai vinto!", True, (pygame.Color('black')))
    punteggiofinale=font.render(f"Punteggio: {point}", True, (pygame.Color('black')))
    screen.blit(vittoria, (280,280))
    screen.blit(punteggiofinale, (250,350))
    aggiorna()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    inizializza()
                    return
#-- loop di gioco --

while True:
    ball_x += vel_x
    ball_y += vel_y
    screen.fill(pygame.Color('white'))
    disegna()
    aggiorna_hitbox()
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        base_x -= base_vel
    if keys[pygame.K_RIGHT]:
        base_x += base_vel

    if ball_x <= margine_x or ball_x >= 800-ball_r-margine_x:
        vel_x = -vel_x
    if ball_y - ball_r<= margine_x :
        vel_y = -vel_y    
    #evita di far uscire la base dallo schermo
    if base_x<0:
        base_x=0
    if base_x>700:
        base_x=700
    if ball_rect.bottom >= 600:
        stop()
    else: 
        rimbalzo()
    for mattoncino in mattoncini[:]:
        if ball_rect.colliderect(mattoncino):
            mattoncini.remove(mattoncino)
            vel_y = -vel_y
            point += 1
            suono_punto.play()
            screen.fill(pygame.Color('white'))
            disegna()
            aggiorna()
            break
    if not mattoncini :
        disegna()
        aggiorna()
        win()


    aggiorna()
    


