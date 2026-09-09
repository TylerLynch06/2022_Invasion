##10/07/2021
##Pygame Template

##Pygame Libraries


import random
import csv
import os
import pygame
import sys
from tiles import *
from DieselEngine.Diesel_4 import *

##PYGAME INIT------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()


##Screen Size and Frame Rate
screenDim = pygame.display.Info()
WIDTH = screenDim.current_w
HEIGHT = screenDim.current_h
FPS = 30
##Colour Library
BLACK = (0, 0, 0)
WHITE = (255, 255 , 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 255)
BROWN = (150, 75,0)
PINK = (216, 191, 216)
VIOLET = (238,130,238)
ORANGE = (255,215,0)
TRANSPARENT = (0,0,0,0)

##WINDOW CREATION--------------------------------------------------------------------------------
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tile Mapper V2")
clock = pygame.time.Clock()

##Timers-----------------------------------------------------------------------------
ADD_ZOMBIE_FREQ = 20000
AZ_now = 0




    

tilesheet = "Tilesheet 64 Bit.png"

def open_file(file_name,purpose):
    return open(file_name+".txt",purpose)
            
##Camera

##Calls upon the diesel camera class
def Camera_input():
    ##Keys are inverse in order to create the sense of player, not camera, movement
    if keys[pygame.K_s]:
        Camera.shift_up(pygame.sprite.Group.sprites(all_sprites))
    if keys[pygame.K_a]:
        Camera.shift_right(pygame.sprite.Group.sprites(all_sprites))
    if keys[pygame.K_d]:
        Camera.shift_left(pygame.sprite.Group.sprites(all_sprites))
    if keys[pygame.K_w]:
        Camera.shift_down(pygame.sprite.Group.sprites(all_sprites))

####Sprite name must be without a number; if player sprite is Player_sprite_7, write the name as 'Player_sprite', and put the index syntax as '_'
##def sprite_list_retrieve(sprite_name,index_syntax,img_type,f_path,*path):
##    total_path = [f_path]
####    for arg in path(
####    path.split(', ')
####    print(path[0:])
##    num+7 = 7
##    number = 0
##    while True:
##        number = int(number)+1
##        number = str(number)
##        print(sprite_name+index_syntax+number+img_type)


    
def image_retrieve(sprite_name):
    new_img = pygame.image.load(os.path.join("Sprites",sprite_name)).convert()
    return new_img

def sound_retrieve(sound_name):
    new_snd = pygame.mixer.Sound(os.path.join("Sounds",sound_name))
    return new_snd


def True_angle(angle,flipped):
    if angle>=0 and flipped == False:

        True_angle = 360 - angle
    if angle<0 and flipped == False:
        True_angle = angle*-1   
    if angle>=0 and flipped == True:
        True_angle = 90 - angle +90
    if angle<0 and flipped == True:
        True_angle = (angle*-1)+180
    return True_angle

def Bullet_icon_spawn(bullet_img, bullet_amnt,start_x,start_y,*sprite_group):
    x_bias = 0
    bullets_drawn = 0
    bullet_rows = 1
    while True:
        if bullets_drawn==bullet_amnt: break
        
        for y in range(bullet_amnt):
            bullets_drawn+=1
            b = Bullet(start_x+ x_bias,start_y+(15*y),bullet_img)
            for arg in sprite_group:
                arg.add(b)
                
            if bullets_drawn>=10*bullet_rows or bullets_drawn == bullet_amnt: break
        x_bias +=30
        bullet_rows +=1
                
    







##SPRITE IMAGING-----------------------------------------------------------------------------

player_img = image_retrieve("Player test.png")
tracer_img = image_retrieve("bullet tracer.png")
handgun_bullet = pygame.image.load(os.path.join("sprites","UI","Rifle bullet icon.png")).convert()
       
##handgun_bullet = image_retrieve("Handgun bullet icon.png")

number = 0
player_reload_rifle = []
while True:  
    try:        
        player_reload_rifle.append(pygame.image.load(os.path.join("sprites","player","rifle","reload","survivor-reload_rifle_"+str(number)+".png")).convert())
        number+=1
    except FileNotFoundError: break
    
number = 0
player_idle_rifle = []
while True:  
    try:
        player_idle_rifle.append(pygame.image.load(os.path.join("sprites","player","rifle","idle","survivor-idle_rifle_"+str(number)+".png")).convert())
        number+=1
    except FileNotFoundError: break

number = 0
player_shoot_rifle = []
while True:  
    try:
        player_shoot_rifle.append(pygame.image.load(os.path.join("sprites","player","rifle","idle","survivor-shoot_rifle_"+str(number)+".png")).convert())
        number+=1
    except FileNotFoundError: break


number = 0
player_reload_handgun = []
while True:  
    try:        
        player_reload_handgun.append(pygame.image.load(os.path.join("sprites","player","handgun","reload","survivor-reload_handgun_"+str(number)+".png")).convert())
        number+=1
    except FileNotFoundError: break

number = 0
player_idle_handgun = []
while True:  
    try:
        player_idle_handgun.append(pygame.image.load(os.path.join("sprites","player","handgun","idle","survivor-idle_handgun_"+str(number)+".png")).convert())
        number+=1
    except FileNotFoundError: break



player_feet_sheet = []
while True:  
    try:
        player_feet_sheet.append(pygame.image.load(os.path.join("sprites","player","feet","run","survivor-run_"+str(number)+".png")).convert())
        number+=1
    except FileNotFoundError: break

##SOUNDS------------------------------------------------------------------------------------------

Assault_gs = sound_retrieve("Rifle_gs.wav")
Empty_gun = sound_retrieve("Empty_gun_click.wav")
Reload = sound_retrieve("Reload.wav")
             
##SPRITECLASSES--------------------------------------------------------------------------------------              
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_idle_handgun[0]
        Animation.apply_first_sheet(self,player_idle_handgun[0])
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH//2,HEIGHT//2]
        self.flipped = False
        ##Player outline is ((0,0,0)), so black cannot be colour key
        self.image.set_colorkey((1,0,0))
        self.current_anisheet = player_idle_handgun
        self.new_sheet_available = True
        self.True_angle = 0
        
        self.current_magcap = 30
        self.bullets = self.current_magcap


        self.reloading = False
        self.idle = True
        self.shooting = False

        ##1: Pistol
        ##2: Rifle
        ##3: Shotgun
        self.current_gun = 1
        

    def update(self):
##        print(self.reloading)
        if self.reloading == True and self.new_sheet_available == True:
            self.new_sheet_available = False
            Animation.apply_new_sheet(self,self.reloading,player_reload_rifle)
            self.reloading = False
            Reload.play()
            self.bullets = self.current_magcap
            
        elif self.shooting == True and self.new_sheet_available == True:
            self.new_sheet_available = False
            Animation.apply_new_sheet(self,self.shooting,player_shoot_rifle)
            self.shooting = False
               

        Animation.ani_cycle(self, self.current_anisheet ,1, player_idle_rifle)        
        self.orig = self.frame            
        self.image = self.frame

        
        
        if mx<self.rect.x+self.image.get_width()//2 and self.flipped == False:
            self.flipped = True
            
        if mx>=self.rect.x+self.image.get_width()//2 and self.flipped == True:
            self.flipped = False
        
        Angles.centre_rotation(self,mx,my)      
        
        
        self.image.set_colorkey((1,0,0))



    def reload(self):
        print("RELOAD")
        if self.idle == True:
            
            self.reloading = True

    def shoot(self):
        if self.bullets>0 and self.reloading == False and self.new_sheet_available == True:
            
            self.shooting = True
            tracer = Tracer(player.rot,player.rect.x+player.image.get_width()//2,player.rect.y+player.image.get_height()//2)
            all_sprites.add(tracer)
            Hit_scan.trigo_calc(player,20,25,all_sprites,player_proj)
            self.bullets -=1
            Assault_gs.stop()
            Assault_gs.play()
            
        elif self.bullets == 0:
            Empty_gun.stop()
            Empty_gun.play()

class Zombie(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,100))
        self.rect = self.image.get_rect()
        ##if 0 is chosen spawn is x varied, else spawn is y varied
        self.spawn_axis = random.choice([0,1])
        if self.spawn_axis == 1:
            self.rect.centerx = random.randint(-200,WIDTH+200)
            self.rect.centery = random.choice([-200,HEIGHT+200])
        else:
            self.rect.centerx = random.choice([-100,WIDTH+100])
            self.rect.centery = random.randint(-100,HEIGHT+100)
        self.flipped = False
        self.True_angle = 0
        self.speed = 5
        self.image.fill(WHITE)  

    def update(self):
        self.horz = player.rect.centerx - self.rect.centerx
        self.vert = player.rect.centery - self.rect.centery
        self.hyp = math.sqrt(self.horz**2 +self.vert**2)
        
##        self.angle_to_player = math.atan(self.horz/self.vert)

        if self.horz > 0: self.x_invert = 1
        else: self.x_invert =-1
        
        if self.vert > 0: self.y_invert = 1
        else: self.y_invert =-1
        
        try:
            self.gradient = math.sqrt(self.vert**2)/math.sqrt(self.horz**2)
        except ZeroDivisionError:
            self.gradient = 1
        self.horz = self.horz
        self.vert = self.gradient *self.speed
        self.horz *= self.speed
        
        ##Squared to root out negatives
        if self.horz**2> 100: self.horz = self.speed
        if self.vert**2> 100: self.vert = self.speed

        self.rect.x+=self.horz*self.x_invert
        self.rect.y+=self.vert*self.y_invert

        
class Tracer(pygame.sprite.Sprite): 

    def __init__(self, angle,start_x,start_y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = tracer_img
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)

        self.rect.left = start_x
        self.rect.centery = start_y


        Angles.child_centre_rotation(self,player)
        ##The rotation from the func is correct, put the position is not, the code below adjusts it
        ##The added integers are simply a bias to match the gun barrel
        if self.True_angle >270:
            self.rect.x+=self.image.get_width()//2-18
            self.rect.y+=self.image.get_height()//2+28
        elif self.True_angle >180 and self.True_angle <= 270:
            self.rect.x-=self.image.get_width()//2+18
            self.rect.y+=self.image.get_height()//2-28
        elif self.True_angle >90 and self.True_angle <= 180:
            self.rect.x-=self.image.get_width()//2-18
            self.rect.y-=self.image.get_height()//2+28
        elif self.True_angle >0 and self.True_angle <= 90:
            self.rect.x+=self.image.get_width()//2+18
            self.rect.y-=self.image.get_height()//2-28
            
##        Angles.SuFOb_Calc(angle,self,player,player.flipped,20,20)

##        print(self.True_angle)

        self.spawn_time = pygame.time.get_ticks()
        
        
    def update(self):
        if pygame.time.get_ticks()>self.spawn_time+50:
            self.kill()

class Bullet(pygame.sprite.Sprite): 

    def __init__(self, start_x,start_y,image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = start_x
        self.rect.top = start_y
        self.image.set_colorkey((0,0,0))


##Initialise Pygame and Create Window

all_sprites = pygame.sprite.Group()
Tiles_group = pygame.sprite.Group()
Imp_Tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_proj = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
UI_bullet_group = pygame.sprite.Group()

##The map gives the groups of both the impassable tiles, and the passable tiles
map = TileMap("Tilemap 64Bit.csv",tilesheet,Imp_Tiles_group,Tiles_group)

all_sprites.add(Imp_Tiles_group)
all_sprites.add(Tiles_group)

player = Player()
player_group.add(player)

##pf = Player_feet()
##all_sprites.add(pf)

Spawning.loop(Zombie,6,all_sprites,enemy_group)

print(enemy_group)


GAME(FPS,WIDTH,HEIGHT)
TEXT_MAP = UI.Text_map_setup()

## Game Loop ##

running = True
while running:
    ##Mouse finder
    Mouseco = []
    Mouseco = pygame.mouse.get_pos()
    mx = Mouseco[0]
    my = Mouseco[1]
    
    clock.tick(FPS)
    ## 1)Input Process
    keys = pygame.key.get_pressed()

    Camera_input()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            
            if event.key == pygame.K_r: player.reloading = True               


        if event.type == pygame.MOUSEBUTTONUP:

            player.shoot()        
            
    hits = pygame.sprite.groupcollide(enemy_group,player_proj,True,True)
    for hit in hits: Spawning.base_spawn(Zombie,all_sprites,enemy_group)

    ##Timers
    if AZ_now+ADD_ZOMBIE_FREQ<pygame.time.get_ticks():
        Spawning.base_spawn(Zombie, all_sprites,enemy_group)
        AZ_now = pygame.time.get_ticks()
    
    
    ## 2)Update

    

##    UI.add_text(TEXT_MAP, player.magazine, 20,WHITE, "pixelbase.ttf", WIDTH//2,HEIGHT//2) 

    all_sprites.update()
    player_group.update()

    ## 3)render
    screen.fill(BLACK)
##    map.draw_map(screen)


    
    Tiles_group.draw(screen)
    
    
    all_sprites.draw(screen)
    
    player_group.draw(screen)
    Bullet_icon_spawn(handgun_bullet,player.bullets,50,50, UI_bullet_group)
    UI_bullet_group.draw(screen)
    sprite_wiping.Group_wipe(UI_bullet_group)
    ##After every bullet shot, the UI is cleared, and the remaining bullets are redrawn, but one less than it was prior
    ##This does not remove all bullets due to the basics of pygame, it has already been drawn
    ##UI.add_draw_text(screen, player.bullets, 30, WHITE, "Pixelbase.ttf", 50,50)
    
   
    
    ##after render flip display
    pygame.display.flip()

pygame.quit()
