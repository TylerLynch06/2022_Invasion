##10/07/2021
##Pygame Template

##Pygame Libraries


import random
import pygame


    
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
BROWN = (150, 75, 0)
PINK = (216, 191, 216)
VIOLET = (238,130,238)
ORANGE = (255,215,0)
TRANSPARENT = (0,0,0,0)

##TILE MAPPER

Tile_images = []
for number in range(4):
    Tile_images.append(pygame.transform.scale2x(pygame.image.load("Tile"+str(number+1)+".png")))
    
TILE_XANDY = 64
##Purpose is W, A, R
def open_file(file_name,purpose):
    return open(file_name+".txt",purpose)

def Tile_randomiser():
    numberstring = ""
    new_locs = []
    Tile_locs = open_file("Tile_loc","w")
    for number in range(100):
        for i in range(100):
            numberstring = numberstring+str(random.randint(1,4))
            ##print(numberstring)
        Tile_locs.write(numberstring+str("\n"))
        numberstring = ""
            
    Tile_locs.close()
            
##Camera
Camera_pan_dist = 16
class Camera():
    
    def shift_up():
        shiftables = pygame.sprite.Group.sprites(all_sprites)
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.y-=Camera_pan_dist
            
    def shift_down():
        shiftables = pygame.sprite.Group.sprites(all_sprites)
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.y+=Camera_pan_dist   
        
    def shift_left():
        shiftables = pygame.sprite.Group.sprites(all_sprites)
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.x-=Camera_pan_dist        
        
    def shift_right():
        shiftables = pygame.sprite.Group.sprites(all_sprites)
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.x+=Camera_pan_dist

def Camera_input():
    if keys[pygame.K_UP]:
        Camera.shift_up()
    if keys[pygame.K_RIGHT]:
        Camera.shift_right()
    if keys[pygame.K_LEFT]:
        Camera.shift_left()
    if keys[pygame.K_DOWN]:
        Camera.shift_down()            
        
        

def Tile_setup():
    global Tiles
    global Tile_x_len
    global Tile_y_len
    Tile_y_len = 0
    Tiles = []   
    Tile_x_gathered = False
    Tile_location = open_file("Tile_loc","r")
    
    while True:
        a = Tile_location.readline().strip()
        
        if Tile_x_gathered == False:
            Tile_x_len = len(a)
            Tile_x_gathered = True
            
        if not a: break
        Tile_y_len +=1
        a = int(a)
        Tiles.append(a)
        
    Tile_location.close()
    return Tiles, Tile_x_len

def Tile_mapper(Tiles,Tile_x_len,Tile_y_len):
    y_start = 0
    for y in range(Tile_y_len):
        x_start = 0
        for x in range(Tile_x_len):
            ##Must be done in 2 phases to recover ID, as int is non-subscriptable
            ID = str(Tiles[y])
            ID = int(ID[x])
            T = Tile(ID,x_start,y_start)
            Tiles_group.add(T)
            all_sprites.add(T)
            x_start +=TILE_XANDY
        y_start+=TILE_XANDY
            
def Tile_imager(Tile,Tile_id):
    ##Must be sibtracted or else it exceeds list index
    Tile.image.blit(Tile_images[Tile.ID-1],(0,0))  

##Objects

class Tile(pygame.sprite.Sprite):
    
    def __init__(self,tile_id,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_XANDY,TILE_XANDY))
        self.ID = tile_id
        Tile_imager(self,self.ID)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60,60))
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH//2,HEIGHT//2]
        self.image.fill(YELLOW)


##Initialise Pygame and Create Window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Mapper V1")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
Tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

Tile_randomiser()
Tile_setup()
Tile_mapper(Tiles,Tile_x_len,Tile_y_len)

player = Player()
player_group.add(player)

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
            

    ## 2)Update

    all_sprites.update()

    ## 3)render
    screen.fill(WHITE)
    Tiles_group.draw(screen)

    all_sprites.draw(screen)
    player_group.draw(screen)
    
    ##after render flip display
    pygame.display.flip()

pygame.quit()
