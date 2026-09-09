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
        if angle>0 and flipped == False:
            subject.rect.left = object.rect.centerx+x_bias
            subject.rect.bottom = object.rect.centery+y_bias


        if angle<0 and flipped == False:
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
            
##            if mouse_x<self.rect.x+self.image.get_width()//2 and self.flipped == False:
##                self.flipped = True
##            if mx>=self.rect.x+self.image.get_width()//2 and self.flipped == True:
##                self.flipped = False
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
    
