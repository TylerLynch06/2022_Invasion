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
from APPE.All_Purpose_Python_Engine import *

##PYGAME INIT------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()

##Joystick is a list!
joysticks = Controller.controller_setup()
if joysticks == []: Controller_on = False
else: Controller_on = True




##Screen Size and Frame Rate
screenDim = pygame.display.Info()
WIDTH = screenDim.current_w
HEIGHT = screenDim.current_h
FPS = 45
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
DARKBLUE = (0,0,255)
TRANSPARENT = (0,0,0,0)


##WINDOW CREATION--------------------------------------------------------------------------------
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tile Mapper V2")
clock = pygame.time.Clock()

##Timers-----------------------------------------------------------------------------
zombie_freq = 8000
WEAPON_FREQ = 5000
TAUNT_FREQ = 15000
TYPE_FREQ = 100
AZ_now = 0
Type_now = 0
taunt_now = 0
Fire_rate_now = 0

##Misc Player Variables
player_magcap = [8,30,80]
##Fire_rate in ms
player_firerate = [0,150,95]
player_gun_name = ["Handgun","AK-47","M-60"]
Auto_firing = False

##Misc Variables
new_game_now = True
game_over = False
Image_mover = int(0)
Taunts = ["Your boots are covered in blood","You feel like this will never end","The Earth Quakes beneath Your Feet","You pray your gun doesn't jam","The air smells of brass, and iron","You feel like you will not survive",]
Death_taunts = ["Try changing the code, to make it easier","were you even close to the high score?","You can do better, much better.","What else did you expect to happen?","You should have brought some med-kits.","Try running away, since you can't aim."]   

tilesheet = "Tilesheet 64 Bit.png"

def open_file(file_name,purpose):
    return open(file_name+".txt",purpose)
            
##Camera

##Calls upon the diesel camera class
def Camera_input():
    ##Keys are inverse in order to create the sense of player, not camera, movement
    if keys[pygame.K_s]:
        Camera.shift_up(pygame.sprite.Group.sprites(all_sprites))
        if Camera.collision_check(player_group,Imp_Tiles_group): Camera.shift_down(pygame.sprite.Group.sprites(all_sprites))
    if keys[pygame.K_a]:
        Camera.shift_right(pygame.sprite.Group.sprites(all_sprites))
        if Camera.collision_check(player_group,Imp_Tiles_group): Camera.shift_left(pygame.sprite.Group.sprites(all_sprites))
    if keys[pygame.K_d]:
        Camera.shift_left(pygame.sprite.Group.sprites(all_sprites))
        if Camera.collision_check(player_group,Imp_Tiles_group): Camera.shift_right(pygame.sprite.Group.sprites(all_sprites))
    if keys[pygame.K_w]:
        Camera.shift_down(pygame.sprite.Group.sprites(all_sprites))
        if Camera.collision_check(player_group,Imp_Tiles_group): Camera.shift_up(pygame.sprite.Group.sprites(all_sprites))

    if Controller_on == True:
        if Controller_inputs[1]>0.5:
            Camera.shift_up(pygame.sprite.Group.sprites(all_sprites))
        if Controller_inputs[0]<-0.5:
            Camera.shift_right(pygame.sprite.Group.sprites(all_sprites))
        if Controller_inputs[0]>0.5:
            Camera.shift_left(pygame.sprite.Group.sprites(all_sprites))
        if Controller_inputs[1]<-0.5:
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
                
def Player_anim_retrieve(weapon,action,player_action_anim_sheet):
    number = 0
    player_sprite_sheet=[]
    while True:
        try:
            number+=1
            player_sprite_sheet.append((pygame.image.load(os.path.join("sprites","player",weapon,action,"survivor-"+action+"_"+weapon+"_"+str(number)+".png"))).convert())
        except FileNotFoundError: break
    player_action_anim_sheet.append(player_sprite_sheet)

def Zombie_anim_retrieve(action,Zombie_spritesheet):
    number = 0
    sprite_sheet=[]
    while True:
        try:
            number+=1
            sprite_sheet.append((pygame.image.load(os.path.join("sprites","zombie",action,"skeleton-"+action+"_"+str(number)+".png"))).convert())
        except FileNotFoundError: break
    Zombie_spritesheet.append(sprite_sheet)


        
##sound is bool
def blood_splat(x,y,sound):

    if sound:Blood_splats[random.randint(0,1)].play()
    for particle in range(random.randint(5,10)):
        b = Blood(x,y)
        all_sprites.add(b)
        blood_group.add(b)

def Intro():

    global Intro_running
    Intro_running = True
    anitrack = 0
    frametracker = 0
    start_parts = pygame.sprite.Group()
    begun_type = False
    while Intro_running == True:
         clock.tick(45)
         Particles.Moving_axis_img(DARKBLUE,pygame.image.load("rain droplet 2.png"),8,30,15,60,8,5,start_parts,(random.randint(-200,WIDTH),random.randint(-50,-10)),1,1,60)


         ##frametracker, anitrack = Animation.to_screen_ani_cycle(45, anitrack, frametracker,screen,Intro_animation[0],4,Intro_animation[0],0,-300)
         screen.blit(Intro_img,(-400,-300))
         screen.blit(Title_img,(WIDTH//3.49,HEIGHT//3))
         if begun_type == False:
            begun_type = True
         UI.add_draw_text(screen, "By Tyler P. Lynch", 30, WHITE, "Pixelbase.ttf", WIDTH//2.5,HEIGHT//1.4)
  
         start_parts.update()
         start_parts.draw(screen)
         pygame.display.flip()
         for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                w = Intro_wiper()
                w.add(start_parts)
        
def endgame():
    global game_over
    player_death_splat.play()
    for number in range(5):
        blood_splat(player.rect.centerx,player.rect.centery,False)
    player.kill()
    

    sprite_list = pygame.sprite.Group.sprites(enemy_group)
    for sprite in sprite_list:
        blood_splat(sprite.rect.centerx,sprite.rect.centery,False)
        sprite.kill()
    

    HB.kill()

    game_over = True
    UI.Typing_message(screen,60,"YOU'RE DEAD",80,WHITE,"Pixelbase.ttf", WIDTH//2,HEIGHT//2,typing_text_group)
    UI.Typing_message(screen,50,"Press space to try again!",40,BLUE,"Pixelbase.ttf", WIDTH//1.5,HEIGHT//1.5,typing_text_group)
    UI.Typing_message_timed(screen,100000,30,random.choice(Death_taunts), 35, WHITE, "Pixelbase.ttf", WIDTH//14,HEIGHT//1.2,typing_text_group)
       
    






##SPRITE IMAGING-----------------------------------------------------------------------------


player_img = image_retrieve("Player test.png")
tracer_img = image_retrieve("bullet tracer.png")

player_bullets = []

handgun_bullet = pygame.image.load(os.path.join("sprites","UI","Handgun bullet icon.png")).convert()
player_bullets.append(handgun_bullet)
rifle_bullet = pygame.image.load(os.path.join("sprites","UI","Rifle bullet icon.png")).convert()
player_bullets.append(rifle_bullet)
lmg_bullet = pygame.image.load(os.path.join("sprites","UI","lmg bullet icon.png")).convert()
player_bullets.append(lmg_bullet)

Gun_icons = []
handgun_icon = pygame.image.load(os.path.join("sprites","UI","Handgun.png")).convert()
Gun_icons.append(handgun_icon)
rifle_icon = pygame.image.load(os.path.join("sprites","UI","Rifle.png")).convert()
Gun_icons.append(rifle_icon)
LMG_icon = pygame.image.load(os.path.join("sprites","UI","lmg.png")).convert()
Gun_icons.append(LMG_icon)


Bullet_backboard = pygame.image.load(os.path.join("sprites","UI","bullet backboard.png")).convert()

Health_bar_case = pygame.image.load(os.path.join("sprites","UI","health_bar_case.png")).convert()

Health_bar_img = pygame.image.load(os.path.join("sprites","UI","Health_bar.png")).convert()

Title_img = pygame.image.load(os.path.join("sprites","UI","Title.png")).convert()

Intro_img = pygame.image.load(os.path.join("sprites","UI","Intro_img.png")).convert()

QD = pygame.image.load("Quandale Dingle.jpg")
       
##handgun_bullet = image_retrieve("Handgun bullet icon.png")

player_reload = []
player_idle = []
player_shoot = []

Player_anim_retrieve("handgun","reload",player_reload)

Player_anim_retrieve("handgun","idle",player_idle)

Player_anim_retrieve("handgun","shoot",player_shoot)

Player_anim_retrieve("rifle","reload",player_reload)

Player_anim_retrieve("rifle","idle",player_idle)

Player_anim_retrieve("rifle","shoot",player_shoot)


##This is the LMG, but due to a lack of sprites i reused the shotgun

Player_anim_retrieve("shotgun","reload",player_reload)

Player_anim_retrieve("shotgun","idle",player_idle)

##We dont want the LMG to have any shoot anim; this removes from the satisfaction of the gun
Player_anim_retrieve("PURPOSE ERROR","PURPOSE ERROR",player_shoot)


Zombie_ani = []

Zombie_attack = Zombie_anim_retrieve("attack",Zombie_ani)

Zombie_move = Zombie_anim_retrieve("move",Zombie_ani)

number = 0
Intro_animation = []
intro_sheet=[]
while True:
    try:
        number+=1
        ##background is misspelled, too late to fix
        intro_sheet.append((pygame.image.load(os.path.join("sprites","UI","Intro_backgroud"+str(number)+".png"))).convert())
    except FileNotFoundError: break
Intro_animation.append(intro_sheet)





##player_feet_sheet = []
##while True:  
##    try:
##        player_feet_sheet.append(pygame.image.load(os.path.join("sprites","player","feet","run","survivor-run_"+str(number)+".png")).convert())
##        number+=1
##    except FileNotFoundError: break

##SOUNDS------------------------------------------------------------------------------------------
gun_fire_sfx = []
Assault_gs = sound_retrieve("Rifle_gs.wav")
gun_fire_sfx.append(Assault_gs)

Assault_gs = sound_retrieve("Rifle_gs.wav")
gun_fire_sfx.append(Assault_gs)

LMG_gs = sound_retrieve("LMG_gs.wav")
gun_fire_sfx.append(LMG_gs)

Empty_gun = sound_retrieve("Empty_gun_click.wav")
Reload = sound_retrieve("Reload.wav")

Blood_splats = []
Blood_splats.append(sound_retrieve("Blood Hit 1.wav"))
Blood_splats.append(sound_retrieve("Blood Hit 2.wav"))

player_death_splat = sound_retrieve("Player Death Sound.wav")

BG_music = sound_retrieve("Music BG 2.wav")

             
##SPRITECLASSES--------------------------------------------------------------------------------------              
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        ##This is the first frame of the handgun idle
        self.image = player_idle[0][0]
        Animation.apply_first_sheet(self,player_idle[0][0])
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH//2,HEIGHT//2]
        self.flipped = False
        ##Player outline is ((0,0,0)), so black cannot be colour key
        self.image.set_colorkey((1,0,0))
        self.current_anisheet = player_idle[0]
        self.new_sheet_available = True
        self.True_angle = 0
        self.hp = 100  
        

    
        self.reloading = False
        self.idle = True
        self.shooting = False

        self.guns_available = [99,0,0]

        ##0: Pistol
        ##1: Rifle
        ##2: Shotgun
        ##3: LMG
        self.current_gun = 0

        self.current_magcap = player_magcap[self.current_gun]
        self.bullets = self.current_magcap
        

    def update(self):
##        print(self.reloading)
        if self.reloading == True and self.new_sheet_available == True:
            self.new_sheet_available = False
            Animation.apply_new_sheet(self,player_reload[self.current_gun])
            self.reloading = False
            Reload.play()
            self.current_magcap = player_magcap[self.current_gun]
            self.bullets = self.current_magcap
            self.guns_available[self.current_gun]-=1
            
        elif self.shooting == True and self.new_sheet_available == True:
            Animation.apply_new_sheet(self,player_shoot[self.current_gun])
            self.shooting = False
               

        Animation.ani_cycle(self, self.current_anisheet ,1, player_idle[self.current_gun])        
        self.orig = self.frame            
        self.image = self.frame

        
        
        if mx<self.rect.x+self.image.get_width()//2 and self.flipped == False:
            self.flipped = True
            
        if mx>=self.rect.x+self.image.get_width()//2 and self.flipped == True:
            self.flipped = False
        
        Angles.centre_rotation(self,mx,my)      
        
        
        self.image.set_colorkey((1,0,0))

        ##DEATH
        if self.hp<=0:
            endgame()

        self.guns_available[0] = 99


    def reload(self):
        print("RELOAD")
        if self.idle == True and self.bullets != self.current_magcap:
            self.reloading = True

    def shoot(self):
        if self.bullets>0 and self.reloading == False and self.new_sheet_available == True and game_over == False:
            
            self.shooting = True
            tracer = Tracer(player.rot,player.rect.x+player.image.get_width()//2,player.rect.y+player.image.get_height()//2)
            all_sprites.add(tracer)
            Hit_scan.trigo_calc(player,20,25,all_sprites,player_proj)
            self.bullets -=1
            gun_fire_sfx[player.current_gun].stop()
            gun_fire_sfx[player.current_gun].play()

        elif self.bullets == 0 and game_over == False:
            Empty_gun.stop()
            Empty_gun.play()
            UI.Typing_message_timed(screen,1200,20, "Magazine Empty", 35, RED, "Pixelbase.ttf", WIDTH//2.4,HEIGHT//4,typing_text_group)
     


class Zombie(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Zombie_ani[1][0]
        
        self.rect = self.image.get_rect()
        ##if 0 is chosen spawn is x varied, else spawn is y varied
        self.spawn_axis = random.choice([0,1])
        if self.spawn_axis == 1:
            self.rect.centerx = random.randint(-200,WIDTH+200)
            self.rect.centery = random.choice([-200,HEIGHT+200])
        else:
            self.rect.centerx = random.choice([-100,WIDTH+100])
            self.rect.centery = random.randint(-100,HEIGHT+100)


        ##To avoid looking weird, if the zombie spawns outside the map, it is killed
        self.flipped = False
        self.attacking = False
        self.True_angle = 0
        self.speed = 7

        Animation.apply_first_sheet(self,Zombie_ani[1])

        ##Sprite cannot be killed in init, so we must create a bool for later death

            
            
     
    def update(self):

        global score
        ##Hits isnt bool, so this must suffice
        if pygame.sprite.spritecollide(self,Tiles_group,False): pass
        else:
            Spawning.base_spawn(Zombie, all_sprites,enemy_group)
            self.kill()
        
        ##Pathfinding Code
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

        hits = pygame.sprite.spritecollide(self,player_group,False)    
        if hits and self.attacking == False:
            self.attacking = True
            Animation.apply_new_sheet(self,Zombie_ani[0])
        elif hits and self.frame == Zombie_ani[0][3]:
            player.hp -= 10
            ##This is to avoid several consecutive hits, since the parameter is the hit frame from the animation
            self.frame = Zombie_ani[0][7]
        ##Idle Checker
        if self.current_anisheet == Zombie_ani[1]: self.attacking = False
        self.rect.x+=self.horz*self.x_invert
        self.rect.y+=self.vert*self.y_invert
        
        ##Animation
                                     
        Animation.ani_cycle(self, self.current_anisheet ,1, Zombie_ani[1])
        self.image = self.frame
        self.orig = self.frame
        self.image.set_colorkey(BLACK)

        ##Rotation
        ##Due to being based on trigonometry, a flipped variable must be created 
        if player.rect.x<self.rect.x: self.flipped = True
        else: self.flipped = False
        Angles.centre_rotation(self,player.rect.centerx,player.rect.centery)
        


        hits = pygame.sprite.spritecollide(self,player_proj,False)    
        if hits:
            Spawning.base_spawn(Zombie,all_sprites,enemy_group)
            blood_splat(self.rect.centerx,self.rect.centery,True)
            score+=1
            self.kill()


        
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

class Blood(pygame.sprite.Sprite): 

    def __init__(self, start_x,start_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((25,25))
        self.rect = self.image.get_rect()
        self.rect.left = start_x
        self.rect.top = start_y
        self.image.fill((random.randint(180,255),0,0))

        ##Randomises splatter pattern and movement
        self.move_frames = random.randint(5,10)

        self.speed_x = random.choice([random.randint(3,15),random.randint(3,15)*-1])
        self.speed_y = random.choice([random.randint(3,15),random.randint(3,15)*-1])
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self):

        
        if self.move_frames != 0:
            self.rect.x +=self.speed_x
            
            self.rect.y+=self.speed_y

            if self.speed_x<0:self.speed_x+=1
            else: self.speed_x-=1
            if self.speed_y<0:self.speed_y+=1
            else: self.speed_y-=1

            ##Can only move so many frames before stopping
            self.move_frames-=1

##        ##Not exactly zero or height to keep blood around longer
##        if (self.rect.top>HEIGHT*1.5 or self.rect.bottom<-(HEIGHT*0.5) or self.rect.left>WIDTH*1.5 or self.rect.left<-(WIDTH*0.5) or self.spawn_time+15000<pygame.time.get_ticks()) and game_over == False: self.kill()
        if self.spawn_time+15000<pygame.time.get_ticks() and game_over == False: self.kill()
       
##HUD SPRITES
class Health_bar(pygame.sprite.Sprite): 

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        ##We must draw and blit, instead of casting straight to image, as it allows the cropping of the health bar
        self.image = pygame.Surface((player.hp*3,30))
        self.image.blit(Health_bar_img,(0,0))
        self.rect = self.image.get_rect()
        self.rect.center = [600, 80]
        

    def update(self):

        ##This is so that the health bar, is removed, resized, and redrawn
        self.oldleft = self.rect.left
        self.oldy = self.rect.centery
        self.image = pygame.Surface((player.hp*3,30))
        self.rect.left = self.oldleft
        self.rect.centery = self.oldy
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        self.image.blit(Health_bar_img,(0,0))

##Misc
class Pick_up(pygame.sprite.Sprite): 

    def __init__(self):
       pygame.sprite.Sprite.__init__(self)

       if random.randint(1,3) ==3:
           type = 2
       else: type = 1
       self.image = Gun_icons[type]
       self.rect = self.image.get_rect()
       self.spawn_axis = random.choice([0,1])

       if self.spawn_axis == 1:
            self.rect.centerx = random.randint(-200,WIDTH+200)
            self.rect.centery = random.choice([-200,HEIGHT+200])
       else:
            self.rect.centerx = random.choice([-100,WIDTH+100])
            self.rect.centery = random.randint(-100,HEIGHT+100)

       self.image.set_colorkey((255,0,255))

       self.mover = 0
       self.speedy = 1

       self.type = type

       self.image = Transform.Scale(self.image,self,0.6)


    def update(self):

        if pygame.sprite.spritecollide(self,Tiles_group,False): pass
        else:
            p = Pick_up()
            all_sprites.add(p)
            pick_up_group.add(p)
            self.kill()
            
        self.rect.y += self.speedy
        if current_frame%2 == 0:
            if self.speedy>0:
                self.mover+=1
            else:
                self.mover-=1
                
            if self.mover == 7 or self.mover == -7:
                self.speedy*=-1

        if pygame.sprite.spritecollide(self,player_group,False):
             player.guns_available[self.type] +=1
             self.kill()
             
        

        

class Wiper(pygame.sprite.Sprite): 

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        ##We must draw and blit, instead of casting straight to image, as it allows the cropping of the health bar
        self.image = pygame.Surface((WIDTH,HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top=HEIGHT
        self.rect.centerx = WIDTH//2

        self.speedy = -60

        ##To prevent multiple spawns
        self.new_game_lock = False
        

    def update(self):

        global new_game_now 

        self.rect.y +=self.speedy

        if self.rect.top < 0 and self.new_game_lock == False:
            new_game_now=True
            self.new_game_lock = True
        if self.rect.bottom < 0: self.kill()

class Intro_wiper(pygame.sprite.Sprite): 

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        ##We must draw and blit, instead of casting straight to image, as it allows the cropping of the health bar
        self.image = pygame.Surface((WIDTH,HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top=HEIGHT
        self.rect.centerx = WIDTH//2

        self.speedy = -60

        ##To prevent multiple spawns
        self.new_game_lock = False
        

    def update(self):

        global Intro_running

        self.rect.y +=self.speedy

        if self.rect.top < 0 and self.new_game_lock == False:
            Intro_running=False
            self.new_game_lock = True
            screen_wiper_group.add(self)
        if self.rect.bottom < 0: self.kill()

        
##Initialise Pygame and Create Window

all_sprites = pygame.sprite.Group()
Tiles_group = pygame.sprite.Group()
Imp_Tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_proj = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
UI_bullet_group = pygame.sprite.Group()
HUD = pygame.sprite.Group()
blood_group = pygame.sprite.Group()
bg_particles = pygame.sprite.Group()
screen_wiper_group = pygame.sprite.Group()
pick_up_group = pygame.sprite.Group()
typing_text_group = pygame.sprite.Group()
 
##The map gives the groups of both the impassable tiles, and the passable tiles
map = TileMap("Large Tilemap.csv",tilesheet,Imp_Tiles_group,Tiles_group)

all_sprites.add(Imp_Tiles_group)
all_sprites.add(Tiles_group)


##pf = Player_feet()
##all_sprites.add(pf)

##startgame()
##Spawning.loop(Zombie,6,all_sprites,enemy_group)

GAME(FPS,WIDTH,HEIGHT)
TEXT_MAP = UI.Text_map_setup()
current_frame = 0

high_score = File_actions.Read("HIGH_SCORE.txt")


## Game Loop ##

running = True
BG_music.play(-1)
Intro()

while running:

    if new_game_now == True:
        
        if not player_group:
            player = Player()
            player_group.add(player)
        Spawning.loop(Zombie,6,all_sprites,enemy_group)

        AZ_now = pygame.time.get_ticks()
        weap_now = pygame.time.get_ticks()
        taunt_now = pygame.time.get_ticks()

        HB = Health_bar()
        HUD.add(HB)

        zomb_increase_1= False
        zomb_increase_2= False
        zomb_increase_3= False
        Image_mover = 0
        game_over = False
        Mass_sprite_actions.Group_wipe(blood_group,pick_up_group,typing_text_group)
        HIGH_SCORE =int(File_actions.Read("HIGH_SCORE.txt"))
        new_game_now = False
        score = 0
        Auto_firing = False
        UI.Typing_message_timed(screen,4000,60, "Their Invasion has begun...", 35, WHITE, "Pixelbase.ttf", WIDTH//2.7,HEIGHT//3,typing_text_group)


        

        
    ##Mouse finder
    Mouseco = []
    Mouseco = pygame.mouse.get_pos()
    mx = Mouseco[0]
    my = Mouseco[1]
    
    clock.tick(FPS)
    current_frame+=1
    if current_frame>FPS: current_frame = 0

    
    
    ## 1)Input Process
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False

            if event.key == pygame.K_SPACE and game_over ==True:
                w = Wiper()
                screen_wiper_group.add(w)

            
            if game_over == False:
                if event.key == pygame.K_r and player.guns_available[player.current_gun]>0: player.reload()               

                if event.key == pygame.K_1 and player.current_gun!= 0 :
                    player.current_gun = 0
                    player.guns_available[player.current_gun]-=1
                    player.reloading = True            
                if event.key == pygame.K_2 and player.current_gun!= 1 and player.guns_available[1]>0:
                    player.current_gun = 1
                    player.reloading = True
                if event.key == pygame.K_3 and player.current_gun!= 2 and player.guns_available[2]>0:
                    player.current_gun = 2
                    player.reloading = True
                    
                if event.key == pygame.K_4 and player.current_gun!= 3:
                    p = Pick_up()
                    all_sprites.add(p)
                    pick_up_group.add(p)
        if game_over == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_firerate[player.current_gun] != 0:
                        if player.bullets>0:
                            Auto_firing = True
                        else:
                            Empty_gun.play()
                            Auto_firing = False
                            
                    else: player.shoot()

            if event.type == pygame.MOUSEBUTTONUP:
                Auto_firing = False

    if Auto_firing == True and pygame.time.get_ticks()> Fire_rate_now + player_firerate[player.current_gun]:
        try:
            player.shoot()
            Fire_rate_now = pygame.time.get_ticks()
        except AttributeError: Auto_firing = False

##    else: Empty_gun.play()
            
    ##Controller Inputs
    if Controller_on == True:
        Controller_inputs = Controller.dual_joystick_values(joysticks[0])
        Trigger_inputs = Controller.trigger_values(joysticks[0])
        print(Trigger_inputs)

        if Trigger_inputs[0]>0.9:
            player.reloading = True

    if game_over == False:
        Camera_input()

            
            
    ##WORKING BULLET COLLISION IN ZOMBIE CLASS
##    hits = pygame.sprite.groupcollide(enemy_group,player_proj,True,True)
##    for hit in hits: Spawning.base_spawn(Zombie,all_sprites,enemy_group)

    
    ##Timers + Difficulty Scaling + Taunts
    if score>75:
        sprite_list = pygame.sprite.Group.sprites(enemy_group)
        for sprite in sprite_list: sprite.speed = 10
        if zomb_increase_1 == False:
            UI.Typing_message_timed(screen,4000,60, "The Horde grows restless...", 35, WHITE, "Pixelbase.ttf", WIDTH//2.5,HEIGHT//3,typing_text_group)
            zomb_increase_1 = True
            
    if score>250:
        sprite_list = pygame.sprite.Group.sprites(enemy_group)
        for sprite in sprite_list: sprite.speed = 12
        if zomb_increase_2 == False:
            UI.Typing_message_timed(screen,4000,60, "The Horde grows ferocious...", 35, WHITE, "Pixelbase.ttf", WIDTH//2.5,HEIGHT//3,typing_text_group)
            zomb_increase_2 = True
        
    if score>500:
        sprite_list = pygame.sprite.Group.sprites(enemy_group)
        for sprite in sprite_list: sprite.speed = 16
        
        if zomb_increase_3 == False:
            UI.Typing_message_timed(screen,4000,60, "The Horde Approaches...", 35, RED, "Pixelbase.ttf", WIDTH//2.5,HEIGHT//3,typing_text_group)
            zomb_increase_3 = True
            zombie_freq//=4

        
    if AZ_now+zombie_freq<pygame.time.get_ticks() and player.hp >0:
        Spawning.base_spawn(Zombie, all_sprites,enemy_group)
        AZ_now = pygame.time.get_ticks()
        

    if weap_now+WEAPON_FREQ<pygame.time.get_ticks() and player.hp >0:
        p = Pick_up()
        all_sprites.add(p)
        pick_up_group.add(p)
        weap_now = pygame.time.get_ticks()

    if taunt_now+TAUNT_FREQ<pygame.time.get_ticks() and game_over == False:
        UI.Typing_message_timed(screen,2500,20,random.choice(Taunts), 35, WHITE, "Pixelbase.ttf", WIDTH//14,HEIGHT//1.25,typing_text_group)
        taunt_now = pygame.time.get_ticks()   
    
    
    ## 2)Update



    

##    UI.add_text(TEXT_MAP, player.magazine, 20,WHITE, "pixelbase.ttf", WIDTH//2,HEIGHT//2) 

    all_sprites.update()
    player_group.update()
    bg_particles.update()
    screen_wiper_group.update()
##    typing_text_group.update()

    if game_over == False:
        HUD.update()

    ## 3)render

    
    screen.fill(BLACK)
##    map.draw_map(screen) 
    Tiles_group.draw(screen) 
    all_sprites.draw(screen)
    player_group.draw(screen)
    bg_particles.draw(screen)
    

   #User Interface

    ##Bias included to fit health bar
    UI.draw_image(screen,Health_bar_case,HB.rect.left-5,HB.rect.top-5-Image_mover,None)
    HUD.draw(screen)

    if game_over == True:
        if Image_mover<400:
            Image_mover += 9
    UI.draw_image(screen,Bullet_backboard,30,20-Image_mover,((255,0,255)))
    UI.draw_image(screen,Gun_icons[player.current_gun],110,35-Image_mover,(255,0,255))
    ##UI.draw_image(screen,QD,WIDTH//2,HEIGHT//2,None)
    
    Bullet_icon_spawn(player_bullets[player.current_gun],player.bullets,80,140-Image_mover, UI_bullet_group)
    UI_bullet_group.draw(screen)
    Mass_sprite_actions.Group_wipe(UI_bullet_group)
    
    if  current_frame%2 ==  0: Particles.Moving_axis_img(DARKBLUE,pygame.image.load("rain droplet.png"),8,30,15,60,8,5,bg_particles,(random.randint(-200,WIDTH),random.randint(-50,-10)),1,1,60)

    ##Score Processing
    if score>HIGH_SCORE:
        File_actions.Write("HIGH_SCORE.txt",score)

    
    UI.add_draw_text(screen, "Score: "+str(score), 30, WHITE, "Pixelbase.ttf", WIDTH-300+Image_mover,60)
    UI.add_draw_text(screen, "High Score: "+str(HIGH_SCORE), 30, WHITE, "Pixelbase.ttf", WIDTH-300+Image_mover,100)
     
    ##Ammo counter
    UI.add_draw_text(screen, "Magazines:", 30, WHITE, "Pixelbase.ttf", 50-Image_mover,340)
    for number in range(3):
        UI.add_draw_text(screen, str(player_gun_name[number])+": "+str(player.guns_available[number]), 25, WHITE, "Pixelbase.ttf", 100-Image_mover,400+(number*50))
    typing_text_group.update()

    screen_wiper_group.draw(screen)
    ##After every bullet shot, the UI is cleared, and the remaining bullets are redrawn, but one less than it was prior
    ##This does not remove all bullets due to the basics of pygame, it has already been drawn


  
    ##after render flip display
    pygame.display.flip()

pygame.quit()
