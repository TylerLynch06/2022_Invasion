import math
import pygame

class GAME(object):

    def __init__(self,fps,width,height):
        global FPS
        global WIDTH
        global HEIGHT
        FPS = fps
        WIDTH = width
        HEIGHT = height
        
class Angles():

    ##Object to subject calculations
    def ObSu_Calc(object_x,object_y,subject_x,subject_y):

        ##Vertical Line is always Opp, Horizantal is always Adj
        hor_dist = int(subject_x - object_x)
        ver_dist  = int(subject_y - object_y)
        
        ##This is the outcome angle, it must be multiplied as it is given in radians
        ##Must be multiplied by -1 as the desired angle is always inverse of what is wanted
        return (math.atan(ver_dist/hor_dist)*57.296 )

    ##Subject from object (bullet from player)
    ##Flipped assumes right is default
    def SuFOb_Calc(angle, subject, object, flipped,x_bias,y_bias):
        if angle>0:
            subject.rect.left = object.rect.centerx+x_bias
            subject.rect.bottom = object.rect.centery+y_bias


        if angle<0:
            subject.rect.left = object.rect.centerx-x_bias
            subject.rect.top = object.rect.centery+y_bias

            
        if angle>0 and flipped == True:
            subject.rect.right = object.rect.centerx+x_bias
            subject.rect.top = object.rect.centery+y_bias
 

        if angle<0 and flipped == True:
            subject.rect.right = object.rect.centerx-x_bias
            subject.rect.bottom = object.rect.centery+y_bias

    ##Self.orig is equal to first image, before transformation
    ##Main purpose is to rotate player or other sprites
    def centre_rotation(self,mouse_x,mouse_y):
        try:
            ##Zero Divison error is caused within the ObSu calc, where the horizantal distance is == 0
            self.rot = (Angles.ObSu_Calc(self.rect.x+self.image.get_width()//2,self.rect.y+self.image.get_height()//2,mouse_x,mouse_y))
            self.True_angle = Angles.True_angle(self.rot,self.flipped)
            rotated_image = pygame.transform.rotate(self.orig, self.True_angle)
            old_centre=self.rect.center

            self.image = rotated_image
            self.rect = self.image.get_rect() 
            self.rect.center = old_centre
        except ZeroDivisionError: pass

    ##Side cannot be self, it must be 'left' etc
    def child_centre_rotation(self,parent):
        try:
            rotated_image = pygame.transform.rotate(self.orig, parent.True_angle)
            old_centre=parent.rect.center
            self.True_angle = parent.True_angle
            self.image = rotated_image
            self.rect = self.image.get_rect() 
            self.rect.center = old_centre
        except ZeroDivisionError: pass
        
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
    
class Transform():

    ##Give X and Y flip as bool
    def Flip(x_flip,y_flip,image):
        imageF = pygame.transform.flip(image,x_flip,y_flip)

        return imageF

    def Scale(image,sprite,mag):
        width = int((sprite.rect.x*mag)//1)
        height = int((sprite.rect.y*mag)//1)
        imageS = pygame.transform.scale(image,(width,height))
        return imageS

Camera_pan_dist = 20
class Camera():
    
    def shift_up(shiftables):
##            shiftables = pygame.sprite.Group.sprites(all_sprites)
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.y-=Camera_pan_dist
            
    def shift_down(shiftables):
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.y+=Camera_pan_dist   
        
    def shift_left(shiftables):
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.x-=Camera_pan_dist        
        
    def shift_right(shiftables):
        for number in range(len(shiftables)):
            current_sprite = shiftables[number]
            current_sprite.rect.x+=Camera_pan_dist

class Ratio():

    ##To 1
    def ratio_t1(x,y):
        independant_ratio = y/x
        ##why only return one variable? Becuase one variable must always be one
        return independant_ratio

class Animation():

    def ani_cycle(self, sprite_list,frame_delay,flipped):
        self.frametracker+=1
        if self.frametracker>FPS:
            self.frametracker = 0
        try:
            if self.frametracker>frame_delay:
                self.frame = sprite_list[self.anitrack]
##                ##Compared to static images, which must constnatly checked to be flipped, when we create a new frame, it must start off flipped if the previous image was
##                ##in the future, if angles become more accurate, this will be optional
##                if flipped == True:
##                    self.frame = Transform.Flip(True,False,self.frame)
                self.anitrack+=1
                self.frametracker = -1                   
        except IndexError:
            self.anitrack = 1

class Hit_scan():

    class Hit_scanner(pygame.sprite.Sprite):

        def __init__(self,start_x,start_y,dimensions):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((dimensions,dimensions))
            self.rect = self.image.get_rect()
##            if angle>-0.2:
##                x_bias*=-1
            self.rect.centerx = start_x
            self.rect.centery = start_y
            self.image.set_colorkey((0,0,0))
            self.image.fill((255,0,255))
##            if self.rect.left>width or self.rect.right<0 or self.rect.top>height or self.rect.bottom<0: self.kill()
            self.living_frames = 0
##            Player_proj.add(self)
##            all_sprites.add(self)

        def update(self):
            if self.living_frames==3: self.kill()
            else: self.living_frames+=1

    def trigo_calc(parent,biasx,biasy,*groups):

        ##ASSUMES ANGLE 0 IS EQUAL TO 3' OCLOCK

        ##Must be divided as pygame works in radians
        theta = parent.True_angle / 57.296
        
        adj = WIDTH//2
        opp = math.tan(theta)*adj

        distance = int(math.sqrt((adj**2)+(opp**2)))
        if distance>10000: distance//=40

        opp/=adj
        adj =1

        if opp<adj:
            constant= 1/opp 
            opp*=constant
            adj*=constant
        else:
            constant= 1/adj
            opp*=constant
            adj*=constant
            
        distance_persquare = (int(math.sqrt((adj**2)+(opp**2))))

        scanners = distance//distance_persquare
        if parent.True_angle>180:
            adj*=-1
            opp*=-1
            biasx *= -1
        if parent.True_angle>90 and parent.True_angle<270:
            biasy *= -1

        for number in range(scanners):
            new_scanner = Hit_scan.Hit_scanner(parent.rect.centerx+(adj*number)+biasx,parent.rect.centery-(opp*number)+biasy,30)
            for arg in groups: arg.add(new_scanner)


    
