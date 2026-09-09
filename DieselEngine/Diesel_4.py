import math
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

    def manual_single_rotation(self,angle):

        old_centre=self.rect.center
        self.image = pygame.transform.rotate(self.image,angle)
        self.rect = self.image.get_rect() 
        self.rect.center = old_centre

    ##Rotates the same direction as parent class, but using parent's parameters
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
        width = int((sprite.image.get_width()*mag)//1)
        height = int((sprite.image.get_height()*mag)//1)
        imageS = pygame.transform.scale(image,(width,height))
        return imageS

Camera_pan_dist = 25
class Camera():

    def camera_pan_dist():
        return Camera_pan_dist
    
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

    def collision_check(focus_object_group, imp_tile_group):
        
        hits = pygame.sprite.groupcollide(focus_object_group,imp_tile_group,False,False)
        if hits: return True

class Ratio():

    ##To 1
    def ratio_t1(x,y):
        independant_ratio = y/x
        ##why only return one variable? Becuase one variable must always be one
        return independant_ratio

class Animation():

    ##After a purposeful error, the sprite will return to the 'return_sheet'
    ##Return state is so that, after a state is over (like reloading), it will turn back to idle state, further modification is required in the actual sprite class for this to work
    ##Colur key input is just a colour 
    def to_screen_ani_cycle(fps,anitrack, frametracker,screen_surface, sprite_list,frame_delay,return_sheet,x,y):
        frametracker+=1
        if frametracker>FPS:
            frametracker = 0
            
        try:
            if frametracker>frame_delay:
                frame = sprite_list[anitrack]
                anitrack+=1
                frametracker = 0
                screen_surface.blit(frame,(x,y))
                
        except IndexError:
            anitrack = 0
        

        return frametracker, anitrack
                     
    def ani_cycle(self, sprite_list,frame_delay,return_sheet):
        self.frametracker+=1
        if self.frametracker>FPS:
            self.frametracker = 0
        try:
            if self.frametracker>frame_delay:
                self.frame = sprite_list[self.anitrack]
                self.anitrack+=1
                self.frametracker = 0                 
        except IndexError:
            self.anitrack = 0
            self.current_anisheet = return_sheet
            self.new_sheet_available = True
            
            

    def apply_new_sheet(self,new_anisheet):
        self.current_anisheet = new_anisheet
        self.new_sheet_available = False

        self.frametracker = 0
        self.anitrack = 0

    def apply_first_sheet(self, anisheet):
        self.current_anisheet = anisheet
        self.frametracker = 0
        self.anitrack  = 0
        self.frame = self.image


class Hit_scan():

    class Hit_scanner(pygame.sprite.Sprite):

        def __init__(self,start_x,start_y,dimensions):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((dimensions,dimensions))
            self.rect = self.image.get_rect()
            self.rect.centerx = start_x
            self.rect.centery = start_y
            self.image.set_colorkey((0,0,0))
##            self.image.fill((255,0,255))
            self.living_frames = 0

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
        if distance>10000:
            distance//=40
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
            new_scanner = Hit_scan.Hit_scanner(parent.rect.centerx+(adj*number)+biasx,parent.rect.centery-(opp*number)+biasy,20)
            for arg in groups: arg.add(new_scanner)

            

class Spawning():

    def loop(sprite_class, times,*groups):
        for number in range(times):
            new_sprite = sprite_class()
            for arg in groups: 
                arg.add(new_sprite)

    def base_spawn(sprite_class,*groups):
        new_sprite = sprite_class()
        for arg in groups:
            arg.add(new_sprite)

class UI():

    def Text_map_setup():
        Map_surface = pygame.Surface((WIDTH,HEIGHT))
        Map_surface.set_colorkey((0,0,0))
        return Map_surface
        

    ##Map_surface is where all the text is added on, and then, externally, this map is blitted at once, i have found this to be more efficient
    ##The map surface is also why it is called "add_text" and not "draw_text"
    def add_text(Map_Surface, text, size, colour, font_name, x, y):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(str(text), True, colour)
        
        Map_Surface.blit(text_surface,(x,y))

    ##TEXT ON A TEXT MAP CANNOT BE CHANGED!
    def draw_text_map(Screen_surface,Map_surface):
        Map_surface = UI.text_wipe(Map_surface)
        
        Screen_surface.blit(Map_surface,(0,0))

    def add_draw_text(Screen_surface, text, size, colour, font_name, x, y):
        
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(str(text), True, colour)
        
        Screen_surface.blit(text_surface,(x,y))

    def draw_image(Screen_surface,image,x,y,colour_key):
        image.set_colorkey(colour_key)
        Screen_surface.blit(image,(x,y))

    class Typing_message(pygame.sprite.Sprite):

        ##Group does not matter, the class just needs to be updated to be processed, putting it in group is the most efficient way to do this overall
        def __init__(self, surface, interval, message, fontsize,colour,fontname, x_loc,y_loc,*groups):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((0,0))
            self.rect = self.image.get_rect()
            self.interval = interval
            self.message = message
            self.char = 1
            for group in groups:
                group.add(self)
            self.now = pygame.time.get_ticks()
            self.surface = surface
            self.fontsize = fontsize
            self.x_loc = x_loc-((len(message)//2)*fontsize)
            self.y_loc = y_loc-(fontsize//2)
            self.colour = colour
            self.fontname = fontname
            

        def update(self):

            if self.now+self.interval<pygame.time.get_ticks():
                self.now = pygame.time.get_ticks()
                self.char +=1
            
            
            self.typed_message = self.message[:self.char]
            ##print(self.typed_message)
            self.font = pygame.font.Font(self.fontname,self.fontsize)
            text_surface = self.font.render(str(self.typed_message), True, self.colour)
            
            self.surface.blit(text_surface,(self.x_loc,self.y_loc))

    class Typing_message_timed(pygame.sprite.Sprite):

        ##Group does not matter, the class just needs to be updated to be processed, putting it in group is the most efficient way to do this overall
        def __init__(self, surface, lifetime, interval, message, fontsize,colour,fontname, x_loc,y_loc,*groups):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((0,0))
            self.rect = self.image.get_rect()
            self.interval = interval
            self.message = message
            self.char = 1
            for group in groups:
                group.add(self)
            self.now = pygame.time.get_ticks()
            self.surface = surface
            self.fontsize = fontsize
            self.x_loc = x_loc
            self.y_loc = y_loc
            self.colour = colour
            self.fontname = fontname
            self.lifetime = lifetime
            self.now2 = pygame.time.get_ticks()
            

        def update(self):

            if self.now+self.interval<pygame.time.get_ticks():
                self.now = pygame.time.get_ticks()
                self.char +=1
            
            
            self.typed_message = self.message[:self.char]
            ##print(self.typed_message)
            self.font = pygame.font.Font(self.fontname,self.fontsize)
            text_surface = self.font.render(str(self.typed_message), True, self.colour)
            
            self.surface.blit(text_surface,(self.x_loc,self.y_loc))

            if pygame.time.get_ticks()>self.now2+self.lifetime: self.kill()
              


class Mass_sprite_actions():

    def Group_wipe(*groups):
        for arg in groups:
            sprite_list = pygame.sprite.Group.sprites(arg)
            for sprite in sprite_list:
                sprite.kill()

    ##Commented out because it sucks and doesn't work
    ##Requires parameters already in function, parameters limited to co-ordiantes, groups restircted to singular group
##    def Group_wipe_and_func(group,func(,*parameter_of_func):
##        
##        sprite_list = pygame.sprite.Group.sprites(group)
##        for sprite in sprite_list:
##            func
##            sprite.kill()

class Controller():

    def controller_setup():

        pygame.joystick.init()
        ##Initialises a joystick object for each joystick found
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        return joysticks

    ##'Joystick' means entire controller, as controller axis often cover trigger and shoulder buttons
    def joystick_value(gamepad, axis):
        return gamepad.get_axis(axis)
        

    def dual_joystick_values(gamepad):
        #0 = Left X
        #1 = Left Y
        #2 = Right X
        #3 = Right Y
        joystick_axis = []
        for axis in range(4):
            joystick_axis.append(Controller.joystick_value(gamepad, axis))
        LeftX, LeftY, RightX,RightY = joystick_axis[0],joystick_axis[1],joystick_axis[2],joystick_axis[3]
            
            
        return LeftX, LeftY, RightX,RightY

    def trigger_values(gamepad):

        joystick_axis = []
        for axis in range(2):
            joystick_axis.append(Controller.joystick_value(gamepad, axis+4))
        Left_T,Right_T = joystick_axis[0],joystick_axis[1]
            
            
        return Left_T,Right_T

class Particles():

    class Moving_axis_rect(pygame.sprite.Sprite):

        ##Y axis and x axis kill should be from 0 to 2
        def __init__(self,colour,xs_range,xs_lower_bound,ys_range,ys_lower_bound,x_size,y_size,group,center_loc,x_axis_kill,y_axis_kill,angle):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((x_size,y_size))
            self.rect = self.image.get_rect()
            self.rect.center = center_loc
            self.image.fill(colour)
            self.speedx = random.randint(xs_lower_bound,xs_lower_bound+xs_range)
            self.speedy = random.randint(ys_lower_bound,ys_lower_bound+ys_range)
            group.add(self)

            self.xaxis_term = x_axis_kill
            self.yaxis_term = y_axis_kill

            Angles.manual_single_rotation(self,45)

            
            ##Term = terminate
##            if x_axis_kill == 1: self.term_x = 0
##            elif x_axis_kill == 2: self.term_x = WIDTH
##
##            if y_axis_kill == 1: self.term_y = 0
##            elif y_axis_kill == 2: self.term_y = HEIGHT

        def update(self):
            
            self.rect.x+=self.speedx
            self.rect.y+=self.speedy

            if self.rect.right<0 and self.xaxis_term ==1: self.kill()
            elif self.rect.left>WIDTH and self.xaxis_term ==2: self.kill()

    class Moving_axis_img(pygame.sprite.Sprite):

        ##Y axis and x axis kill should be from 0 to 2
        def __init__(self,color_key,img,xs_range,xs_lower_bound,ys_range,ys_lower_bound,x_size,y_size,group,center_loc,x_axis_kill,y_axis_kill,angle):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.center = center_loc
            self.speedx = random.randint(xs_lower_bound,xs_lower_bound+xs_range)
            self.speedy = random.randint(ys_lower_bound,ys_lower_bound+ys_range)
            group.add(self)

            self.xaxis_term = x_axis_kill
            self.yaxis_term = y_axis_kill

            self.image.set_colorkey(color_key)

##            Angles.manual_single_rotation(self,45)
##
            
            ##Term = terminate
##            if x_axis_kill == 1: self.term_x = 0
##            elif x_axis_kill == 2: self.term_x = WIDTH
##
##            if y_axis_kill == 1: self.term_y = 0
##            elif y_axis_kill == 2: self.term_y = HEIGHT

        def update(self):
            
            self.rect.x+=self.speedx
            self.rect.y+=self.speedy

            if self.rect.right<0 and self.xaxis_term ==2:
                self.kill()
            elif self.rect.left>WIDTH and self.xaxis_term ==1:
                self.kill()
            if self.rect.bottom<0 and self.yaxis_term ==2:
                self.kill()
            elif self.rect.top>HEIGHT and self.yaxis_term ==1:
                self.kill()

##class Typing():
##
##    class Typing_message(pygame.sprite.Sprite):
##
##        def __init__(self, interval, message, group,x_loc,y_loc, fontsize):
##            pygame.sprite.Sprite.__init__(self)
##            self.interval = interval
##            self.message = message
##            self.char = 1
##            group.add(self)
##            self.now = pygame.time.get_ticks()
##            
##
##        def update(self):
##
##            if self.now+self.interval<pygame.time.get_ticks():
##                self.now = pygame.time.get_ticks()
##                self.char +=1
##            self.typed_message = self.message[:self.char]
##            UI.add_draw_text(screen, str(self.typed_message), fontsize, x_loc,y_loc)           
            
    def message(full_string,current_char):
        current_char +=1
        string = full_string[:current_char]
        return string, current_char

        

    


        


        
        

    


        
        


    
