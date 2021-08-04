'''
Meteor Shooter by Parth Gupta 
Video Game
'''

print ("Use WASD to move and spacebar to shoot lasers, hit enemies and gain points. Don't forget to dodge the meteors!")


import pygame.mixer
import random
from pygame.locals import *
pygame.font.init()
pygame.init()


clock = pygame.time.Clock()
FPS = 60


screenWidth = 800
screenHeight = 800
screen = pygame.display.set_mode((screenWidth,screenHeight))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

red_player_start = pygame.image.load('Resources/playerShip1_red.png')
red_player = pygame.transform.scale(red_player_start, (85,60))
red_player_laser = pygame.image.load('Resources/laserRed03.png')
player_laser_width, player_laser_height = red_player_laser.get_size()
playerWidth, playerHeight = red_player.get_size()



start_enemy_ship = pygame.image.load('Resources/enemyBlue1.png')
enemy_ship = pygame.transform.scale(start_enemy_ship, (60, 60))
enemy_laser = pygame.image.load('Resources/laserBlue06.png')
enemy_laser_width, enemy_laser_height = enemy_laser.get_size()
enemyWidth = 60
enemyHeight = 60


start_meteor = pygame.image.load('Resources/meteorBrown_med1.png')
meteor = pygame.transform.scale(start_meteor, (70,70))
meteor_width, meteor_height = meteor.get_size()


font = pygame.font.SysFont('timesnewroman', 25, True, False)
font2 = pygame.font.SysFont('timesnewroman', 80, True, False)


score = 0
lives = 3
time = 0

laserSound = pygame.mixer.Sound('Resources/laser.wav')
laserSound.set_volume(0.01)
blastSound = pygame.mixer.Sound('Resources/blast.wav')
blastSound.set_volume(0.1)


class Laser:
    def __init__(self, x, y, picture):
        self.x = x 
        self.y = y
        self.picture = picture  
    
    def draw(self, screen):
        screen.blit (self.picture, (self.x, self.y))
    
    def move(self, speed):
        self.y += speed


class Ship:   
    '''
    Superclass designed so that the player and enemy class can inherit from it. It contains
    general methods used by both the player and enemy.
    '''

    timer = 60 
    
    def __init__ (self, x, y, health = 100):
        self.x = x 
        self.y = y
        self.health = health
        self.alive = False 
        self.laserImage = None
        self.laser_list = [] 
        self.shipImage = None 
        self.laserTimer = 0 
    
    def draw(self, screen):
        screen.blit(self.shipImage, (self.x, self.y))
        for laser in self.laser_list:  
            laser.draw(screen)
            
    def laser_move(self, speed):
        self.laser_timer() 
        for laser in self.laser_list:
            laser.move(speed)
            if laser.y > screenHeight or laser.y < 0: 
                self.laser_list.pop(self.laser_list.index(laser)) 
        
    # Timer made to prevent spamming of lasers   
    def laser_timer(self):
        if self.laserTimer >= self.timer: 
            self.laserTimer = 0 
        elif self.laserTimer > 0: 
            self.laserTimer += 1  
        
    def shoot(self): 
        if self.laserTimer == 0: 
            laser = Laser(self.x + (playerWidth/2), self.y, self.laserImage) 
            self.laser_list.append(laser) 
            self.laserTimer = 1 
            
            
class Player(Ship): 
    def __init__ (self, x, y, health = 100): 
        super().__init__(x, y, health) 
        self.shipImage = red_player 
        self.laserImage = red_player_laser
        self.total_health = health
        self.alive = True 
        

class Enemy(Ship):
    timer = 30 
    
    def __init__ (self, x, y, health = 10):
        super().__init__(x,y, health)
        self.shipImage = enemy_ship
        self.laserImage = enemy_laser
        self.total_health = health 
    
    def move(self, speed):
        self.y += speed 


class Meteor:
    start_meteor = pygame.image.load('Resources/meteorBrown_big1.png')
    meteor = pygame.transform.scale(start_meteor, (70,70))
      
    def __init__ (self, x, y):
        self. x = x
        self.y = y 
        self.alive = False 
    
    def move(self, speed):
        self.y += speed
    
    def draw(self, screen):
        screen.blit(self.meteor, (self.x, self.y))
        

class Star: 
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y 
        self.colour = colour
        self.star_vel = 1 
    
    def move(self):
        self.y += self.star_vel
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), 0)

    
def redrawGameScreen(): 
    screen.fill(BLACK)
    for star in stars: 
        star.draw(screen)
        
    for enemy in enemies_max: 
        if enemy.alive: 
            enemy.draw(screen) 
    
    for meteor in meteors: 
        if meteor.alive: 
            meteor.draw(screen)  
    
    player.draw(screen) 
    text = font.render('Score: ' + str(score), False, WHITE) 
    screen.blit(text, (0, 0))
    text2 = font.render('Lives: ' + str(lives), False, WHITE)
    screen.blit(text2, (700, 0))
    text3 = font.render('Health: ' + str(player.health), False, WHITE)
    screen.blit(text3, (670,30))
    pygame.display.flip() 


def quitGame():
    screen.fill(BLACK)
    gameOver = font2.render('Game Over!', False, WHITE)
    screen.blit(gameOver, (200, 350))
    pygame.display.flip()
    pygame.time.delay(1000) 
    pygame.quit()


player = Player(300, 700) 
player_speed = 5 
player_laser_speed = -5 
enemies_max = []
enemy_speed = 2
enemy_laser_speed = 6

meteors = []
meteor_speed = 2


wave_length = 2


stars = []  
for i in range(30):
    star = Star(random.randrange(0, screenWidth), random.randrange(-900, -100), WHITE)
    stars.append(star) 


gameOn = True 
while gameOn:
    clock.tick(FPS) 
    time += 1
    if time == 600:  
        wave_length += 1 
        time = 0 
    
    # Make enemies if they are gone from the screen
    if len(enemies_max) == 0: 
        for i in range(wave_length):
            enemy = Enemy(random.randrange(0, screenWidth - enemyWidth), random.randrange(-2000, -700)) #create enemeies
            enemy.alive = True 
            enemies_max.append(enemy) 
    
    # Make meteors if they are gone from the screen
    if len(meteors) == 0: 
        for i in range(wave_length):
            meteor = Meteor(random.randrange(0, screenWidth), random.randrange(-1000, -100)) #create meteors 
            meteor.alive = True 
            meteors.append(meteor) 
            
    if player.health == 0: 
        if lives > 0: 
            lives -= 1 
            player.health = 100 
    if lives == 0 and player.health == 0: 
        quitGame() 
  
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            gameOn = False  
    
    keys = pygame.key.get_pressed() 
    
    # Player movement 
    if keys[K_w] and player.y - player_speed > 0:
        player.y -= player_speed
    if keys[K_a] and player.x - player_speed > 0:
        player.x -= player_speed 
    if keys[K_d] and player.x + player_speed + playerWidth < screenWidth: 
        player.x += player_speed 
    if keys[K_s] and player.y + player_speed + playerHeight < screenHeight:
        player.y += player_speed 
    if keys[K_SPACE]:
        player.shoot()  
        laserSound.play() 
    player.laser_move(player_laser_speed) 

    # Check if a laser hits an enemy and increase the score if so   
    for laser in player.laser_list: 
        for enemy in enemies_max: 
            if laser.x + player_laser_width > enemy.x and laser.x < enemy.x + enemyWidth and laser.y < enemy.y + enemyHeight and laser.y + player_laser_height > enemy.y:
                score += 10 
                blastSound.play() 
                enemies_max.pop(enemies_max.index(enemy)) 
                player.laser_list.pop(player.laser_list.index(laser)) 
    
    # Check if an enemy hits the player and decrease player health if so
    for enemy in enemies_max: 
        enemy.shoot() 
        enemy.laser_move(enemy_laser_speed)
        enemy.move(enemy_speed) 
        if enemy.y > screenHeight: 
            enemies_max.pop(enemies_max.index(enemy))              
        for laser in enemy.laser_list:  
            if laser.x + enemy_laser_width > player.x and laser.x < player.x + playerWidth and laser.y + enemy_laser_height > player.y and laser.y < player.y + playerHeight:
                    player.health -= 10 
                    enemy.laser_list.pop(enemy.laser_list.index(laser))
                
    # Check if meteors hit the player and decrease player health if so
    for meteor in meteors: 
        meteor.move(meteor_speed) 
        if meteor.x + meteor_width > player.x and meteor.x < player.x + playerWidth and meteor.y + meteor_height > player.y and meteor.y < player.y + playerHeight: 
            if player.health >= 20: 
                player.health -= 20 
                meteors.pop(meteors.index(meteor)) 
                
            elif player.health < 20: 
                if lives > 0: 
                    lives -= 1 
                    player.health = 100  
                    meteors.pop(meteors.index(meteor)) 
        if meteor.y > screenHeight: 
            meteors.pop(meteors.index(meteor)) 
        
        
    # For background
    for star in stars: 
        star.move() 
        if star.y == screenHeight: 
            star.x = random.randrange(0, screenWidth - 6) 
            star.y = 0 
    
    redrawGameScreen()     
            
            
pygame.quit() 
