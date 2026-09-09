##10/07/2021
##Pygame Template

##Pygame Libraries


import random
import csv
import os
import pygame
import sys
from tiles import *
from DieselEngine.Diesel_3 import *

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

def animation_startup(self,starting_image):
    self.frametracker = 0
    self.anitrack = 0
    self.frame = starting_image





##SPRITE IMAGING-----------------------------------------------------------------------------

player_img = image_retrieve("Player test.png")
tracer_img = image_retrieve("bullet tracer.png")

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

##SOUNDS------------------------------------------------------------------------------------------

Assault_gs = sound_retrieve("Rifle_gs.wav")

##class Hit_scan():
##
##    class Hit_scanner(pygame.sprite.Sprite):
##
##        def __init__(self,start_x,start_y,dimensions):
##            pygame.sprite.Sprite.__init__(self)
##            self.image = pygame.Surface((dimensions,dimensions))
##            self.rect = self.image.get_rect()
####            if angle>-0.2:
####                x_bias*=-1
##            self.rect.centerx = start_x
##            self.rect.centery = start_y
##            self.image.set_colorkey((0,0,0))
##            self.image.fill((255,0,255))
####            if self.rect.left>width or self.rect.right<0 or self.rect.top>height or self.rect.bottom<0: self.kill()
##            self.living_frames = 0
####            Player_proj.add(self)
####            all_sprites.add(self)
##
##        def update(self):
##            if self.living_frames==3: self.kill()
##            else: self.living_frames+=1
##
##    def trigo_calc(parent,biasx,biasy,*groups):
##
##        ##ASSUMES ANGLE 0 IS EQUAL TO 3' OCLOCK
##
##        ##Must be divided as pygame works in radians
##        theta = parent.True_angle / 57.296
##        
##        adj = WIDTH//2
##        opp = math.tan(theta)*adj
##
##        distance = int(math.sqrt((adj**2)+(opp**2)))
##        if distance>10000: distance//=40
##
##        opp/=adj
##        adj =1
##
##        if opp<adj:
##            constant= 1/opp 
##            opp*=constant
##            adj*=constant
##        else:
##            constant= 1/adj
##            opp*=constant
##            adj*=constant
##            
##        distance_persquare = (int(math.sqrt((adj**2)+(opp**2))))
##
##        scanners = distance//distance_persquare
##        if parent.True_angle>180:
##            adj*=-1
##            opp*=-1
##            biasx *= -1
##        if parent.True_angle>90 and parent.True_angle<270:
##            biasy *= -1
##
##        for number in range(scanners):
##            new_scanner = Hit_scan.Hit_scanner(parent.rect.centerx+(adj*number)+biasx,parent.rect.centery-(opp*number)+biasy,30)
##            for arg in groups: arg.add(new_scanner)
##
             
##SPRITECLASSES--------------------------------------------------------------------------------------              
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        animation_startup(self,player_idle_rifle[0])
        self.image = player_idle_rifle[0]
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH//2,HEIGHT//2]
        self.flipped = False
        ##Player outline is ((0,0,0)), so black cannot be colour key
        self.image.set_colorkey((1,0,0))
        

    def update(self):

        


        Animation.ani_cycle(self, player_idle_rifle,2,self.flipped)        
        self.orig = self.frame            
        self.image = self.frame

        
        
        if mx<self.rect.x+self.image.get_width()//2 and self.flipped == False:
            self.flipped = True
            
        if mx>=self.rect.x+self.image.get_width()//2 and self.flipped == True:
            self.flipped = False
        
        Angles.centre_rotation(self,mx,my)      
        
        
        self.image.set_colorkey((1,0,0))



    def reload(self): self.reloading = True       

##class Bullet(pygame.sprite.Sprite):
##
##    def __init__(self, start_x,start_y,mouse_x,mouse_y):
##        pygame.sprite.Sprite.__init__(self)
##
##        
##        
##        self.image = pygame.Surface((20,20))
##        self.rect = self.image.get_rect()
##        self.image.fill(WHITE)
##
##        self.rect.centerx = start_x
##        self.rect.centery = start_y
##        
##        self.speed = 15
##        self.angle = math.atan(mouse_y-start_y/mouse_x-start_x)*57.296 
##        print(self.angle)
##        self.x_vel = math.cos(self.angle) * self.speed
##        self.y_vel = math.sin(self.angle) * self.speed
##        print(self.x_vel)
##        print(self.y_vel)
##
##    def update(self):
##        self.rect.x+=int(self.x_vel)
##        self.rect.y+=int(self.y_vel)
        
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



##Initialise Pygame and Create Window

all_sprites = pygame.sprite.Group()
Tiles_group = pygame.sprite.Group()
Imp_Tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_proj = pygame.sprite.Group()

##Tile_randomiser()
##Tile_setup()
##Tile_mapper(Tiles,Tile_x_len,Tile_y_len)

player = Player()
player_group.add(player)

##The map gives the groups of both the impassable tiles, and the passable tiles
map = TileMap("Tilemap 64Bit.csv",tilesheet,Imp_Tiles_group,Tiles_group)

all_sprites.add(Imp_Tiles_group)
all_sprites.add(Tiles_group)

GAME(FPS,WIDTH,HEIGHT)

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
                

##OLD STYLE CAMERA           
##            if event.key == pygame.K_UP:
##                Camera.shift_up()
##            if event.key == pygame.K_DOWN:
##                Camera.shift_down()
##            if event.key == pygame.K_LEFT:
##                Camera.shift_left()
##            if event.key == pygame.K_RIGHT:
##                Camera.shift_right()

        if event.type == pygame.MOUSEBUTTONUP:
            Assault_gs.stop()
            Assault_gs.play()
            tracer = Tracer(player.rot,player.rect.x+player.image.get_width()//2,player.rect.y+player.image.get_height()//2)
            all_sprites.add(tracer)
            Hit_scan.trigo_calc(player,20,25,all_sprites,player_proj)           
##            Hit_scan.Pythag(player.rect.centerx,player.rect.centery,mx,my,WIDTH,HEIGHT,20,30,player.rot,tracer)
##            
            

    ## 2)Update

    all_sprites.update()
    player_group.update()

    ## 3)render
    screen.fill(BLACK)
##    map.draw_map(screen)
    Tiles_group.draw(screen)

    all_sprites.draw(screen)
    player_group.draw(screen)

    
    ##after render flip display
    pygame.display.flip()

pygame.quit()
