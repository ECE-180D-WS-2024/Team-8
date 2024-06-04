import math
import random
import pygame
from pygame.math import Vector2
from src.utils import get_mask_rect
import src.utils
from PIL import Image
from .object import Object
from src.particles import ParticleManager, Fire
from src.bullet import StaffBullet
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from src.localization import capture_frame

cap = cv.VideoCapture(0)
#img_mask = your target detected mask of frame; X's Y's are the coordinate of your target frame
def weaponAngle(img_mask,y1,y2,x1,x2,pre_angle):
    angle = pre_angle
    area = 0
    swingArea = 500
    contours,hierarchy = cv.findContours(img_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt) 
        #Try increase the sensitivity by increase the diversity of angle (orientation) 180/6=30
        if(area > swingArea):
            if(x1 == 0 and x2 == 250 and y1 == 0 and y2 == 43):
                angle = 345
            if(x1 == 0 and x2 == 250 and y1 == 43 and y2 == 86):
                angle = 330
            if(x1 == 0 and x2 == 250 and y1 == 86 and y2 == 129):
                angle = 315
            if(x1 == 0 and x2 == 250 and y1 == 129 and y2 == 172):
                angle = 300
            if(x1 == 0 and x2 == 250 and y1 == 172 and y2 == 215):
                angle = 285
            if(x1 == 0 and x2 == 250 and y1 == 215 and y2 == 258):
                angle = 270
            if(x1 == 0 and x2 == 250 and y1 == 258 and y2 == 301):
                angle = 255
            if(x1 == 0 and x2 == 250 and y1 == 301 and y2 == 344):
                angle = 240
            if(x1 == 0 and x2 == 250 and y1 == 344 and y2 == 387):
                angle = 225
            if(x1 == 0 and x2 == 250 and y1 == 387 and y2 == 430):
                angle = 210
            if(x1 == 0 and x2 == 250 and y1 == 430 and y2 == 480):
                angle = 195
            if(x1 == 250 and x2 == 390 and y1 == 240 and y2 == 480):
                angle = 180
            if(x1 == 250 and x2 == 390 and y1 == 0 and y2 == 240):
                angle = 0
            if(x1 == 390 and x2 == 640 and y1 == 0 and y2 == 43):
                angle = 15
            if(x1 == 390 and x2 == 640 and y1 == 43 and y2 == 86):
                angle = 30
            if(x1 == 390 and x2 == 640 and y1 == 86 and y2 == 129):
                angle = 45
            if(x1 == 390 and x2 == 640 and y1 == 129 and y2 == 172):
                angle = 60
            if(x1 == 390 and x2 == 640 and y1 == 172 and y2 == 215):
                angle = 75
            if(x1 == 390 and x2 == 640 and y1 == 215 and y2 == 258):
                angle = 90
            if(x1 == 390 and x2 == 640 and y1 == 258 and y2 == 301):
                angle = 105
            if(x1 == 390 and x2 == 640 and y1 == 301 and y2 == 344):
                angle = 120
            if(x1 == 390 and x2 == 640 and y1 == 344 and y2 == 387):
                angle = 135
            if(x1 == 390 and x2 == 640 and y1 == 387 and y2 == 430):
                angle = 150
            if(x1 == 390 and x2 == 640 and y1 == 430 and y2 == 480):
                angle = 165

    return angle,area



class WeaponSwing:
    left_swing = 10
    right_swing = -190

    def __init__(self, weapon):
        self.weapon = weapon
        self.angle = 0
        self.offset = Vector2(0, -50)
        self.offset_rotated = Vector2(0, -25)
        self.counter = 0
        self.attack_area = 0
        self.swing_side = 1

    def reset(self):
        self.counter = 0

    def rotate(self, weapon=None):
        position = self.weapon.player.hitbox.center
        if(self.weapon.player.name == "player2"):
            lower_yellow = np.array([20,100,100])
            upper_yellow = np.array([40,255,255]) 
            lower_green = np.array([65,100,100])
            upper_green = np.array([85,255,255])
            lower_blue = np.array([110,255,255])
            upper_blue = np.array([130,255,255])

            lower_color = lower_green
            upper_color = upper_green

            if(self.swing_side == 1):
                _,frame = cap.read()
                #self.clock.tick(self.fps)

                angle15_hsv = cv.cvtColor(frame[0:43,390:640], cv.COLOR_BGR2HSV)
                angle30_hsv = cv.cvtColor(frame[43:86,390:640], cv.COLOR_BGR2HSV)
                angle45_hsv = cv.cvtColor(frame[86:129,390:640], cv.COLOR_BGR2HSV)
                angle60_hsv = cv.cvtColor(frame[129:172,390:640], cv.COLOR_BGR2HSV)
                angle75_hsv = cv.cvtColor(frame[172:215,390:640], cv.COLOR_BGR2HSV)
                angle90_hsv = cv.cvtColor(frame[215:258,390:426], cv.COLOR_BGR2HSV)
                angle105_hsv = cv.cvtColor(frame[258:301,390:640], cv.COLOR_BGR2HSV)
                angle120_hsv = cv.cvtColor(frame[301:344,390:640], cv.COLOR_BGR2HSV)
                angle135_hsv = cv.cvtColor(frame[344:387,390:640], cv.COLOR_BGR2HSV)
                angle150_hsv = cv.cvtColor(frame[387:430,390:640], cv.COLOR_BGR2HSV)
                angle165_hsv = cv.cvtColor(frame[430:480,390:640], cv.COLOR_BGR2HSV)
                angle0_hsv = cv.cvtColor(frame[0:240,250:390], cv.COLOR_BGR2HSV)
                angle180_hsv = cv.cvtColor(frame[0:240,250:390], cv.COLOR_BGR2HSV)
                angle195_hsv = cv.cvtColor(frame[430:480,0:250], cv.COLOR_BGR2HSV) 
                angle210_hsv = cv.cvtColor(frame[387:430,0:250], cv.COLOR_BGR2HSV)
                angle225_hsv = cv.cvtColor(frame[344:387,0:250], cv.COLOR_BGR2HSV)
                angle240_hsv = cv.cvtColor(frame[301:344,0:250], cv.COLOR_BGR2HSV)           
                angle255_hsv = cv.cvtColor(frame[258:301,0:250], cv.COLOR_BGR2HSV)
                angle270_hsv = cv.cvtColor(frame[215:258,0:250], cv.COLOR_BGR2HSV)
                angle285_hsv = cv.cvtColor(frame[172:215,0:250], cv.COLOR_BGR2HSV)
                angle300_hsv = cv.cvtColor(frame[129:172,0:250], cv.COLOR_BGR2HSV)
                angle315_hsv = cv.cvtColor(frame[86:129,0:250], cv.COLOR_BGR2HSV)
                angle330_hsv = cv.cvtColor(frame[43:86,0:250], cv.COLOR_BGR2HSV)
                angle345_hsv = cv.cvtColor(frame[0:43,0:250], cv.COLOR_BGR2HSV)


                angle15_mask = cv.inRange(angle15_hsv,lower_color, upper_color)
                angle45_mask = cv.inRange(angle45_hsv,lower_color, upper_color)
                angle75_mask = cv.inRange(angle75_hsv,lower_color, upper_color)
                angle105_mask = cv.inRange(angle105_hsv,lower_color, upper_color)
                angle135_mask = cv.inRange(angle135_hsv,lower_color, upper_color)
                angle165_mask = cv.inRange(angle165_hsv,lower_color, upper_color)
                angle195_mask = cv.inRange(angle195_hsv,lower_color, upper_color)
                angle225_mask = cv.inRange(angle225_hsv,lower_color, upper_color)  
                angle255_mask = cv.inRange(angle255_hsv,lower_color, upper_color)
                angle285_mask = cv.inRange(angle285_hsv,lower_color, upper_color)
                angle315_mask = cv.inRange(angle315_hsv,lower_color, upper_color)
                angle345_mask = cv.inRange(angle345_hsv,lower_color, upper_color)           
                angle30_mask = cv.inRange(angle30_hsv,lower_color, upper_color)
                angle60_mask = cv.inRange(angle60_hsv,lower_color, upper_color)
                angle90_mask = cv.inRange(angle90_hsv,lower_color, upper_color)
                angle120_mask = cv.inRange(angle120_hsv,lower_color, upper_color)
                angle150_mask = cv.inRange(angle150_hsv,lower_color, upper_color)
                angle0_mask = cv.inRange(angle0_hsv,lower_color, upper_color)
                angle180_mask = cv.inRange(angle180_hsv,lower_color, upper_color)
                angle210_mask = cv.inRange(angle210_hsv,lower_color, upper_color)  
                angle240_mask = cv.inRange(angle240_hsv,lower_color, upper_color)
                angle270_mask = cv.inRange(angle270_hsv,lower_color, upper_color)
                angle300_mask = cv.inRange(angle300_hsv,lower_color, upper_color)
                angle330_mask = cv.inRange(angle330_hsv,lower_color, upper_color) 

                angle,area15 = weaponAngle(angle15_mask,0,43,390,640,self.angle)
                angle,area30 = weaponAngle(angle30_mask,43,86,390,640,angle)
                angle,area45 = weaponAngle(angle45_mask,86,129,390,640,angle)
                angle,area60 = weaponAngle(angle60_mask,129,172,390,640,angle)
                angle,area75 = weaponAngle(angle75_mask,172,215,390,640,angle)
                angle,area90 = weaponAngle(angle90_mask,215,258,390,640,angle)
                angle,area105 = weaponAngle(angle105_mask,258,301,390,640,angle)
                angle,area120 = weaponAngle(angle120_mask,301,344,390,640,angle)
                angle,area135 = weaponAngle(angle135_mask,344,387,390,640,angle)
                angle,area150 = weaponAngle(angle150_mask,430,480,390,640,angle)
                angle,area165 = weaponAngle(angle165_mask,430,480,390,640,angle)
                angle,area0 = weaponAngle(angle0_mask,0,240,250,390,angle)
                angle,area180 = weaponAngle(angle180_mask,240,480,0,250,angle)
                angle,area195 = weaponAngle(angle195_mask,430,480,0,250,angle)
                angle,area210 = weaponAngle(angle210_mask,387,430,0,250,angle)
                angle,area225 = weaponAngle(angle225_mask,344,387,0,250,angle)
                angle,area240 = weaponAngle(angle240_mask,301,344,0,250,angle)
                angle,area255 = weaponAngle(angle255_mask,258,301,0,250,angle)
                angle,area270 = weaponAngle(angle270_mask,215,258,0,250,angle)
                angle,area285 = weaponAngle(angle285_mask,172,215,0,250,angle)
                angle,area300 = weaponAngle(angle300_mask,129,172,0,250,angle)
                angle,area315 = weaponAngle(angle315_mask,86,129,0,250,angle)
                angle,area330 = weaponAngle(angle330_mask,43,86,0,250,angle)
                angle,area345 = weaponAngle(angle345_mask,0,43,0,250,angle)             

                self.attack_area = max(area30,area60,area90,area120,area150,area180,area0,area210,area240,area270,area300,area330,area15,area45,area75,area105,area135,area165,area195,area225,area255,area285,area315,area345)
                self.angle = angle
            else:
                _,frame = cap.read()
                #self.clock.tick(self.fps)
                angle15_hsv = cv.cvtColor(frame[0:43,390:640], cv.COLOR_BGR2HSV)
                angle30_hsv = cv.cvtColor(frame[43:86,390:640], cv.COLOR_BGR2HSV)
                angle45_hsv = cv.cvtColor(frame[86:129,390:640], cv.COLOR_BGR2HSV)
                angle60_hsv = cv.cvtColor(frame[129:172,390:640], cv.COLOR_BGR2HSV)
                angle75_hsv = cv.cvtColor(frame[172:215,390:640], cv.COLOR_BGR2HSV)
                angle90_hsv = cv.cvtColor(frame[215:258,390:426], cv.COLOR_BGR2HSV)
                angle105_hsv = cv.cvtColor(frame[258:301,390:640], cv.COLOR_BGR2HSV)
                angle120_hsv = cv.cvtColor(frame[301:344,390:640], cv.COLOR_BGR2HSV)
                angle135_hsv = cv.cvtColor(frame[344:387,390:640], cv.COLOR_BGR2HSV)
                angle150_hsv = cv.cvtColor(frame[387:430,390:640], cv.COLOR_BGR2HSV)
                angle165_hsv = cv.cvtColor(frame[430:480,390:640], cv.COLOR_BGR2HSV)
                angle0_hsv = cv.cvtColor(frame[0:240,250:390], cv.COLOR_BGR2HSV)
                angle180_hsv = cv.cvtColor(frame[0:240,250:390], cv.COLOR_BGR2HSV)
                angle195_hsv = cv.cvtColor(frame[430:480,0:250], cv.COLOR_BGR2HSV) 
                angle210_hsv = cv.cvtColor(frame[387:430,0:250], cv.COLOR_BGR2HSV)
                angle225_hsv = cv.cvtColor(frame[344:387,0:250], cv.COLOR_BGR2HSV)
                angle240_hsv = cv.cvtColor(frame[301:344,0:250], cv.COLOR_BGR2HSV)           
                angle255_hsv = cv.cvtColor(frame[258:301,0:250], cv.COLOR_BGR2HSV)
                angle270_hsv = cv.cvtColor(frame[215:258,0:250], cv.COLOR_BGR2HSV)
                angle285_hsv = cv.cvtColor(frame[172:215,0:250], cv.COLOR_BGR2HSV)
                angle300_hsv = cv.cvtColor(frame[129:172,0:250], cv.COLOR_BGR2HSV)
                angle315_hsv = cv.cvtColor(frame[86:129,0:250], cv.COLOR_BGR2HSV)
                angle330_hsv = cv.cvtColor(frame[43:86,0:250], cv.COLOR_BGR2HSV)
                angle345_hsv = cv.cvtColor(frame[0:43,0:250], cv.COLOR_BGR2HSV)


                angle15_mask = cv.inRange(angle15_hsv,lower_color, upper_color)
                angle45_mask = cv.inRange(angle45_hsv,lower_color, upper_color)
                angle75_mask = cv.inRange(angle75_hsv,lower_color, upper_color)
                angle105_mask = cv.inRange(angle105_hsv,lower_color, upper_color)
                angle135_mask = cv.inRange(angle135_hsv,lower_color, upper_color)
                angle165_mask = cv.inRange(angle165_hsv,lower_color, upper_color)
                angle195_mask = cv.inRange(angle195_hsv,lower_color, upper_color)
                angle225_mask = cv.inRange(angle225_hsv,lower_color, upper_color)  
                angle255_mask = cv.inRange(angle255_hsv,lower_color, upper_color)
                angle285_mask = cv.inRange(angle285_hsv,lower_color, upper_color)
                angle315_mask = cv.inRange(angle315_hsv,lower_color, upper_color)
                angle345_mask = cv.inRange(angle345_hsv,lower_color, upper_color)           
                angle30_mask = cv.inRange(angle30_hsv,lower_color, upper_color)
                angle60_mask = cv.inRange(angle60_hsv,lower_color, upper_color)
                angle90_mask = cv.inRange(angle90_hsv,lower_color, upper_color)
                angle120_mask = cv.inRange(angle120_hsv,lower_color, upper_color)
                angle150_mask = cv.inRange(angle150_hsv,lower_color, upper_color)
                angle0_mask = cv.inRange(angle0_hsv,lower_color, upper_color)
                angle180_mask = cv.inRange(angle180_hsv,lower_color, upper_color)
                angle210_mask = cv.inRange(angle210_hsv,lower_color, upper_color)  
                angle240_mask = cv.inRange(angle240_hsv,lower_color, upper_color)
                angle270_mask = cv.inRange(angle270_hsv,lower_color, upper_color)
                angle300_mask = cv.inRange(angle300_hsv,lower_color, upper_color)
                angle330_mask = cv.inRange(angle330_hsv,lower_color, upper_color) 

                angle,area15 = weaponAngle(angle15_mask,0,43,390,640,self.angle)
                angle,area30 = weaponAngle(angle30_mask,43,86,390,640,angle)
                angle,area45 = weaponAngle(angle45_mask,86,129,390,640,angle)
                angle,area60 = weaponAngle(angle60_mask,129,172,390,640,angle)
                angle,area75 = weaponAngle(angle75_mask,172,215,390,640,angle)
                angle,area90 = weaponAngle(angle90_mask,215,258,390,640,angle)
                angle,area105 = weaponAngle(angle105_mask,258,301,390,640,angle)
                angle,area120 = weaponAngle(angle120_mask,301,344,390,640,angle)
                angle,area135 = weaponAngle(angle135_mask,344,387,390,640,angle)
                angle,area150 = weaponAngle(angle150_mask,430,480,390,640,angle)
                angle,area165 = weaponAngle(angle165_mask,430,480,390,640,angle)
                angle,area0 = weaponAngle(angle0_mask,0,240,250,390,angle)
                angle,area180 = weaponAngle(angle180_mask,240,480,0,250,angle)
                angle,area195 = weaponAngle(angle195_mask,430,480,0,250,angle)
                angle,area210 = weaponAngle(angle210_mask,387,430,0,250,angle)
                angle,area225 = weaponAngle(angle225_mask,344,387,0,250,angle)
                angle,area240 = weaponAngle(angle240_mask,301,344,0,250,angle)
                angle,area255 = weaponAngle(angle255_mask,258,301,0,250,angle)
                angle,area270 = weaponAngle(angle270_mask,215,258,0,250,angle)
                angle,area285 = weaponAngle(angle285_mask,172,215,0,250,angle)
                angle,area300 = weaponAngle(angle300_mask,129,172,0,250,angle)
                angle,area315 = weaponAngle(angle315_mask,86,129,0,250,angle)
                angle,area330 = weaponAngle(angle330_mask,43,86,0,250,angle)
                angle,area345 = weaponAngle(angle345_mask,0,43,0,250,angle) 

                self.attack_area = max(area30,area60,area90,area120,area150,area180,area0,area210,area240,area270,area300,area330,area15,area45,area75,area105,area135,area165,area195,area225,area255,area285,area315,area345)
                self.angle = angle

        if weapon:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.image, self.angle, 1)
        else:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)

        offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + offset_rotated)
        self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)
        self.offset_rotated = Vector2(0, -35).rotate(-self.angle)

    def swing(self):
         #weapon swing range
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        swingrange = 6
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.angle += swingrange * self.swing_side
        position = self.weapon.player.hitbox.center
        self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)
        offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + offset_rotated)
        # self.rect_mask = get_mask_rect(self.image, *self.rect.topleft)
        self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)
        self.counter += 1

class Weapon(Object):
    def __init__(self, game, name=None, size=None, room=None, position=None):
        self.scale = 3
        Object.__init__(self, game, name, 'weapon', size, room, position)
        self.size = size
        self.player = None
        self.load_image()
        if position:
            self.rect.x, self.rect.y = position[0], position[1]
        self.time = 0
        self.weapon_swing = WeaponSwing(self)
        self.starting_position = [self.hitbox.bottomleft[0] - 1, self.hitbox.bottomleft[1]]
        self.angle = 0

    def load_image(self):
        """Load weapon image and initialize instance variables"""
        self.size = tuple(self.scale * x for x in Image.open(f'./assets/objects/weapon/{self.name}/{self.name}.png').size)
        self.original_image = pygame.image.load(f'./assets/objects/weapon/{self.name}/{self.name}.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image_picked = pygame.image.load(f'./assets/objects/weapon/{self.name}/picked_{self.name}.png').convert_alpha()
        self.image_picked = pygame.transform.scale(self.image_picked, self.size)
        self.hud_image = pygame.image.load(f'./assets/objects/weapon/{self.name}/{self.name}_hud.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.original_image, *self.rect.topleft)

    def detect_collision(self):
        if self.game.player.hitbox.colliderect(self.rect) or self.game.player2.hitbox.colliderect(self.rect):
            self.image = self.image_picked
            self.interaction = True
        else:
            self.image = self.original_image
            self.interaction = False
            self.show_name.reset_line_length()

    def interact(self,name):
        self.weapon_swing.reset()
        if(name == "player"):
            self.player = self.game.player
        elif(name == "player2"):
            self.player = self.game.player2
        self.player.items.append(self)
        if not self.player.weapon:
            self.player.weapon = self
        if self.room == self.game.world_manager.current_room:
            self.room.objects.remove(self)
        self.interaction = False
        self.show_name.reset_line_length()
        self.game.sound_manager.play_get_item_sound()

    def drop(self):
        self.game.sound_manager.play_drop_sound()
        self.room = self.game.world_manager.current_room
        self.player.items.remove(self)
        self.player.weapon = None
        self.game.world_manager.current_room.objects.append(self)
        if self.player.items:
            self.player.weapon = self.player.items[-1]
        self.load_image()
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.player = None
        self.weapon_swing.offset_rotated = Vector2(0, -25)

    def enemy_collision(self):
        for enemy in self.game.enemy_manager.enemy_list:
            if (
                    pygame.sprite.collide_mask(self.game.player.weapon, enemy)
                    and enemy.dead is False
                    and enemy.can_get_hurt_from_weapon()
            ):  
                if(self.game.player.weapon.name != "staff"):
                    self.game.player.weapon.special_effect(enemy)
                enemy.hurt = True
                enemy.hp -= self.game.player.weapon.damage * self.game.player.strength
                enemy.entity_animation.hurt_timer = pygame.time.get_ticks()
                self.game.sound_manager.play_hit_sound()
                enemy.weapon_hurt_cooldown = pygame.time.get_ticks()
            elif(
                    pygame.sprite.collide_mask(self.game.player2.weapon, enemy)
                    and enemy.dead is False
                    and enemy.can_get_hurt_from_weapon()
            ):
                if(self.game.player2.weapon.name != "staff"):
                    self.game.player2.weapon.special_effect(enemy)
                enemy.hurt = True
                enemy.hp -= self.game.player2.weapon.damage * self.game.player2.strength
                enemy.entity_animation.hurt_timer = pygame.time.get_ticks()
                self.game.sound_manager.play_hit_sound()
                enemy.weapon_hurt_cooldown = pygame.time.get_ticks()

    def player_update(self):
        self.interaction = False
        if self.weapon_swing.counter == 10:
            self.original_image = pygame.transform.flip(self.original_image, 1, 0)
            self.player.attacking = False
            self.weapon_swing.counter = 0
        if self.player.attacking and self.weapon_swing.counter <= 10:
            self.weapon_swing.swing()
            self.enemy_collision()
        else:
            self.weapon_swing.rotate()

    def draw_shadow(self, surface):
        if self.dropped:
            self.shadow.set_shadow_position()
            self.shadow.draw_shadow(surface)
        else:
            if not self.shadow.shadow_set:
                self.shadow.set_shadow_position()
            if self.player:
                self.shadow.shadow_set = False
            if self.player is None:
                self.shadow.draw_shadow(surface)

    def update(self):
        self.hovering.hovering()
        if self.player:
            self.player_update()
        else:
            self.show_price.update()
            self.update_bounce()
        self.update_hitbox()

    def draw(self):
        surface = self.room.tile_map.map_surface
        if self.player:
            surface = self.game.screen
        surface.blit(self.image, self.rect)
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        self.show_price.draw(surface)
        self.draw_shadow(surface)

class Staff(Weapon):
    name = 'staff'
    damage = 10
    size = (30, 96)

    def __init__(self, game, room=None, position=None):
        super().__init__(game, self.name, self.size, room, position)
        self.value = 150
        self.animation_frame = 0
        self.images = []
        self.load_images()
        self.firing_position = self.hitbox.topleft
        self.bullets = []
        self.shadow.set_correct(3)

    def load_images(self):
        for i in range(4):
            image = pygame.image.load(f'./assets/objects/weapon/{self.name}/{self.name}{i}.png').convert_alpha()
            image = pygame.transform.scale(image, self.size)
            self.images.append(image)
        self.image = self.images[0]

    def calculate_firing_position(self):
        if 0 <= self.weapon_swing.angle < 90:
            self.firing_position = self.hitbox.topleft
        elif 90 <= self.weapon_swing.angle < 180:
            self.firing_position = (self.hitbox.bottomleft[0], self.hitbox.bottomleft[1] - 15)
        elif 270 <= self.weapon_swing.angle < 360:
            self.firing_position = self.hitbox.topright
        else:
            self.firing_position = (self.hitbox.bottomright[0], self.hitbox.bottomright[1] - 15)

    def fire(self):
        if(self.weapon_swing.angle == 0):
            pos = [677,7]
        if(self.weapon_swing.angle == 15):
            pos = [522,12]
        if(self.weapon_swing.angle == 30):
            pos = [423,14]
        if(self.weapon_swing.angle == 45):
            pos = [308,13]
        if(self.weapon_swing.angle == 60):
            pos = [38,19]
        if(self.weapon_swing.angle == 75):
            pos = [5,278]
        if(self.weapon_swing.angle == 90):
            pos = [2,417]
        if(self.weapon_swing.angle == 105):
            pos = [5,554]
        if(self.weapon_swing.angle == 120):
            pos = [0,633]
        if(self.weapon_swing.angle == 135):
            pos = [409,708]
        if(self.weapon_swing.angle == 150):
            pos = [492,711]
        if(self.weapon_swing.angle == 165):
            pos = [588,694]
        if(self.weapon_swing.angle == 180):
            pos = [657,707]
        if(self.weapon_swing.angle == 195):
            pos = [765,709]
        if(self.weapon_swing.angle == 210):
            pos = [835,708]
        if(self.weapon_swing.angle == 225):
            pos = [959,708]
        if(self.weapon_swing.angle == 240):
            pos = [1076,653]
        if(self.weapon_swing.angle == 255):
            pos = [1074,494]
        if(self.weapon_swing.angle == 270):
            pos = [1076,429]
        if(self.weapon_swing.angle == 285):
            pos = [1074,364]
        if(self.weapon_swing.angle == 300):
            pos = [1074,225]
        if(self.weapon_swing.angle == 315):
            pos = [1074,48]    
        if(self.weapon_swing.angle == 330):
            pos = [931,4]
        if(self.weapon_swing.angle == 345):
            pos = [794,5]  
        self.update_hitbox()
        self.calculate_firing_position()
        self.game.bullet_manager.add_bullet(
            StaffBullet(self.game, self, self.game.world_manager.current_room, self.firing_position[0],
                        self.firing_position[1], pos, self.player.name))
        self.game.sound_manager.play(pygame.mixer.Sound('./assets/sound/Shoot6.wav'))

    def player_update(self):
        self.interaction = False
        self.weapon_swing.rotate(self)
        if self.player.attacking:
            self.fire()
            self.player.attacking = False

    def animate(self):
        self.animation_frame += 1.5 / 15
        if self.animation_frame > 4:
            self.animation_frame = 0
        self.image = self.images[int(self.animation_frame)]

    def update(self):
        self.hovering.hovering()
        self.animate()
        if self.player:
            self.player_update()
        else:
            self.show_price.update()
            self.update_bounce()
        self.update_hitbox()

    def draw(self):
        surface = self.room.tile_map.map_surface
        if self.player:
            surface = self.game.screen
        surface.blit(self.image, self.rect)
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        self.show_price.draw(surface)
        self.draw_shadow(surface)


class AnimeSword(Weapon):
    name = 'anime_sword'
    damage = 40
    size = (36, 90)

    def __init__(self, game, room=None, position=None):
        super().__init__(game, self.name, self.size, room, position)
        self.value = 100
        self.damage_enemies = []
        self.shadow.set_correct(-3)

    class Slash:
        def __init__(self, enemy, weapon):
            self.enemy = enemy
            self.weapon = weapon
            self.damage = 0.1

        def update(self):
            self.enemy.hp -= self.weapon.damage * self.damage
            self.update_damage()

        def update_damage(self):
            self.damage += 0.1

        def draw(self):
            pass
    
    '''
    def screen_shake(self):
        self.game.screen_position = (random.randint(-3, 3), random.randint(-3, 3))
    '''

    def enemy_in_list(self, enemy):
        for e in self.damage_enemies:
            if e.enemy is enemy:
                return True

    def special_effect(self, enemy):
        for e in self.damage_enemies:
            if e.enemy is enemy:
                e.update()
        if not self.enemy_in_list(enemy):
            self.damage_enemies.append(self.Slash(enemy, self))

    def player_update(self):
        self.interaction = False
        if self.weapon_swing.counter == 10:
            self.original_image = pygame.transform.flip(self.original_image, 1, 0)
            self.player.attacking = False
            self.weapon_swing.counter = 0
            self.game.screen_position = (0, 0)
        if self.player.attacking and self.weapon_swing.counter <= 10:
            self.weapon_swing.swing()
            self.enemy_collision()
            self.game.sound_manager.play_sword_sound()
            #self.screen_shake()
        else:
            self.weapon_swing.rotate()


class FireSword(Weapon):
    name = 'fire_sword'
    damage = 30
    size = (36, 90)

    def __init__(self, game, room=None, position=None):
        super().__init__(game, self.name, self.size, room, position)
        self.value = 150
        self.burning_enemies = []

    class Burn:
        def __init__(self, game, enemy, weapon):
            self.game = game
            self.enemy = enemy
            self.weapon = weapon
            self.counter = 0
            self.tick = 0
            self.damage = 5 * self.game.player.strength

        def get_enemy(self):
            return self.enemy

        def update(self):
            if self.tick == 30 and self.counter < 5:
                self.enemy.hp -= self.damage
                self.tick = 0
                self.counter += 1
            self.tick += 1
            if self.counter == 5:
                self.unburn()

        def unburn(self):
            self.weapon.burning_enemies.remove(self)

        def draw(self):
            self.game.particle_manager.add_fire_particle(
                Fire(self.game, self.enemy.rect.center[0] / 4, self.enemy.rect.center[1] / 4, 'enemy'))

    def special_effect(self, enemy):
        self.burning_enemies.append(self.Burn(self.game, enemy, self))

    def player_update(self):
        self.interaction = False
        if self.weapon_swing.counter == 10:
            self.original_image = pygame.transform.flip(self.original_image, 1, 0)
            self.player.attacking = False
            self.weapon_swing.counter = 0
        if self.player.attacking and self.weapon_swing.counter <= 10:
            self.weapon_swing.swing()
            self.enemy_collision()
            self.game.sound_manager.play_sword_sound('fire')
        else:
            self.weapon_swing.rotate()

    def update(self):
        self.hovering.hovering()
        self.burning()
        if self.player:
            self.player_update()
        else:
            self.show_price.update()
            self.update_bounce()
        self.update_hitbox()
        for e in self.burning_enemies:
            e.update()
            e.draw()

    def burning(self):
        x, y = self.weapon_swing.offset_rotated.xy
        x = self.rect.center[0] + x
        y = self.rect.center[1] + y
        if self.game.world_manager.switch_room is False:
            self.game.particle_manager.add_fire_particle(Fire(self.game, x / 4, y / 4))
