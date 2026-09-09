import pygame
import random

class GAME(object):

    def __init__(self,fps,width,height):
        global FPS
        global WIDTH
        global HEIGHT
        FPS = fps
        WIDTH = width
        HEIGHT = height
        
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
