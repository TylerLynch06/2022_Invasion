##10/07/2021
##Pygame Template

##Pygame Libraries


import random
import csv
import os
import pygame
import sys
from tiles import *
from DieselEngine.Diesel import *


    
##Screen Size and Frame Rate
WIDTH = 1280
HEIGHT = 640
FPS = 30
##Colour Library
BLACK = (0, 0, 0)
WHITE = (255, 255 , 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 255)
BROWN = (150, 75,
         0)
PINK = (216, 191, 216)
VIOLET = (238,130,238)
ORANGE = (255,215,0)
TRANSPARENT = (0,0,0,0)

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

def image_retrieve(sprite_name):
    new_img = pygame.image.load(os.path.join("Sprites",sprite_name)).convert()
    return new_img

##PYGAME INIT------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Mapper V2")
clock = pygame.time.Clock()

##SPRITE IMAGING-----------------------------------------------------------------------------

player_img = image_retrieve("Player test.png")
tracer_img = image_retrieve("bullet tracer.png")


##CLASSES--------------------------------------------------------------------------------------              
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH//2,HEIGHT//2]
##        self.image.blit(self.image(0,0))
        self.orig = self.image
        self.flipped = False
        self.image.set_colorkey(WHITE)

    def update(self):

        if mx<self.rect.x+self.image.get_width()//2 and self.flipped == False:
            self.orig = Transform.Flip(True,False,self.orig)
            self.flipped = True
        if mx>=self.rect.x+self.image.get_width()//2 and self.flipped == True:
            self.orig = Transform.Flip(True,False,self.orig)
            self.flipped = False
            
        ##Half of size must be added as based location is from topright
        try:
            ##Zero Divison error is caused within the ObSu calc, where the horizantal distance is == 0
            self.rot = (Angles.ObSu_Calc(self.rect.x+self.image.get_width()//2,self.rect.y+self.image.get_height()//2,mx,my))
            ##print((Angles.ObSu_Calc(self.rect.x+self.image.get_width()//2,self.rect.y+self.image.get_height()//2,mx,my)))
            rotated_image = pygame.transform.rotate(self.orig, self.rot)
            old_centre=self.rect.center
            self.image = rotated_image
            self.rect = self.image.get_rect() 
            self.rect.center = old_centre
        except ZeroDivisionError: pass



class Tracer(pygame.sprite.Sprite):

    def __init__(self, angle,start_x,start_y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = tracer_img
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)

        self.rect.centerx = start_x
        self.rect.centery = start_y
        
        rotated_image = pygame.transform.rotate(self.orig, angle)
        old_centre=self.rect.center
        self.image = rotated_image
        self.rect = self.image.get_rect()
        self.rect.center = old_centre

        Angles.SuFOb_Calc(angle,self,player,player.flipped)




        self.spawn_time = pygame.time.get_ticks()
        
    def update(self):
        if pygame.time.get_ticks()>self.spawn_time+250:
            self.kill()



##Initialise Pygame and Create Window

all_sprites = pygame.sprite.Group()
Tiles_group = pygame.sprite.Group()
Imp_Tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

##Tile_randomiser()
##Tile_setup()
##Tile_mapper(Tiles,Tile_x_len,Tile_y_len)

player = Player()
player_group.add(player)

##The map gives the groups of both the impassable tiles, and the passable tiles
map = TileMap("Tilemap 64Bit.csv",tilesheet,Imp_Tiles_group,Tiles_group)

all_sprites.add(Tiles_group)


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
            
            if event.key == pygame.K_UP:
                Camera.shift_up()
            if event.key == pygame.K_DOWN:
                Camera.shift_down()
            if event.key == pygame.K_LEFT:
                Camera.shift_left()
            if event.key == pygame.K_RIGHT:
                Camera.shift_right()

        if event.type == pygame.MOUSEBUTTONUP:
            tracer = Tracer(player.rot,player.rect.x+player.image.get_width()//2,player.rect.y+player.image.get_height()//2)
            all_sprites.add(tracer)
            
            

    ## 2)Update

    all_sprites.update()
    player_group.update()

    ## 3)render
    screen.fill(WHITE)
##    map.draw_map(screen)
    Tiles_group.draw(screen)

    all_sprites.draw(screen)
    player_group.draw(screen)
    
    
    ##after render flip display
    pygame.display.flip()

pygame.quit()
