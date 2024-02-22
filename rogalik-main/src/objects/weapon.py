#OpenCV
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Pygame
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

cap = cv.VideoCapture(0)
#img_mask = your target detected mask of frame; X's Y's are the coordinate of your target frame
def weaponAngle(img_mask,y1,y2,x1,x2,pre_angle):
    angle = pre_angle
    detectArea = 1000
    contours,hierarchy = cv.findContours(img_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt) 
        #Try increase the sensitivity by increase the diversity of angle (orientation) 180/6=30
        if(area > detectArea):
            if(x1 == 0 and x2 == 213 and y1 == 0 and y2 == 96):
                angle = 330
            if(x1 == 0 and x2 == 213 and y1 == 96 and y2 == 192):
                angle = 300
            if(x1 == 0 and x2 == 213 and y1 == 192 and y2 == 288):
                angle = 270
            if(x1 == 0 and x2 == 213 and y1 == 288 and y2 == 384):
                angle = 240
            if(x1 == 0 and x2 == 213 and y1 == 384 and y2 == 480):
                angle = 210
            if(x1 == 213 and x2 == 426 and y1 == 320 and y2 == 480):
                angle = 180
            if(x1 == 213 and x2 == 426 and y1 == 0 and y2 == 160):
                angle = 0
            if(x1 == 426 and x2 == 640 and y1 == 384 and y2 == 480):
                angle = 150
            if(x1 == 426 and x2 == 640 and y1 == 288 and y2 == 384):
                angle = 120
            if(x1 == 426 and x2 == 640 and y1 == 192 and y2 == 288):
                angle = 90
            if(x1 == 426 and x2 == 640 and y1 == 96 and y2 == 192):
                angle = 60
            if(x1 == 426 and x2 == 640 and y1 == 0 and y2 == 96):
                angle = 30
    return angle

#Weapon Control(Localization)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class WeaponSwing:
    def __init__(self, weapon):
        self.weapon = weapon
        self.angle = 0
        self.offset = Vector2(0, -50)
        self.offset_rotated = Vector2(0, -25)
        self.counter = 0
        self.swing_side = 1

    def reset(self):
        self.counter = 0

    def rotate(self, weapon=None):
        #Mouse cursor Orientation Control---------------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
        mx, my = pygame.mouse.get_pos()
        if self.swing_side == 1:
        #self.angle = angle where weapon orientated
            #self.angle = (180 / math.pi) * math.atan2(-self.swing_side * dy, dx) + self.left_swing
            self.angle = 0
        else:
            #self.angle = (180 / math.pi) * math.atan2(self.swing_side * dy, dx) + self.right_swing
            self.angle = 0
        '''
        #OpenCV Orientation Control---------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # define range of blue color in HSV
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([40,255,255]) 
        lower_green = np.array([50,100,100])
        upper_green = np.array([70,255,255])

        lower_color = lower_yellow
        upper_color = upper_yellow

        if(self.swing_side == 1):
            _, frame = cap.read()

            angle30_hsv = cv.cvtColor(frame[0:96,426:640], cv.COLOR_BGR2HSV)
            angle60_hsv = cv.cvtColor(frame[96:192,426:640], cv.COLOR_BGR2HSV)
            angle90_hsv = cv.cvtColor(frame[192:288,426:640], cv.COLOR_BGR2HSV)
            angle120_hsv = cv.cvtColor(frame[288:384,426:640], cv.COLOR_BGR2HSV)
            angle150_hsv = cv.cvtColor(frame[384:480,426:640], cv.COLOR_BGR2HSV)
            angle0_hsv = cv.cvtColor(frame[0:160,213:426], cv.COLOR_BGR2HSV)
            angle180_hsv = cv.cvtColor(frame[320:480,213:426], cv.COLOR_BGR2HSV)
            angle210_hsv = cv.cvtColor(frame[384:480,0:213], cv.COLOR_BGR2HSV)
            angle240_hsv = cv.cvtColor(frame[288:384,0:213], cv.COLOR_BGR2HSV) 
            angle270_hsv = cv.cvtColor(frame[192:288,0:213], cv.COLOR_BGR2HSV)
            angle300_hsv = cv.cvtColor(frame[96:192,0:213], cv.COLOR_BGR2HSV)
            angle330_hsv = cv.cvtColor(frame[0:96,0:213], cv.COLOR_BGR2HSV)                 

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

            angle = weaponAngle(angle30_mask,0,96,426,640,self.angle)
            angle = weaponAngle(angle60_mask,96,192,426,640,angle)
            angle = weaponAngle(angle90_mask,192,288,426,640,angle)
            angle = weaponAngle(angle120_mask,288,384,426,640,angle)
            angle = weaponAngle(angle150_mask,384,480,426,640,angle)
            angle = weaponAngle(angle0_mask,0,160,213,426,angle)
            angle = weaponAngle(angle180_mask,320,480,213,426,angle)
            angle = weaponAngle(angle210_mask,384,480,0,213,angle)
            angle = weaponAngle(angle240_mask,288,384,0,213,angle)
            angle = weaponAngle(angle270_mask,192,288,0,213,angle)
            angle = weaponAngle(angle300_mask,96,192,0,213,angle)
            angle = weaponAngle(angle330_mask,0,96,0,213,angle)

            self.angle = angle
        else:
            _, frame = cap.read() 

            angle30_hsv = cv.cvtColor(frame[0:96,426:640], cv.COLOR_BGR2HSV)
            angle60_hsv = cv.cvtColor(frame[96:192,426:640], cv.COLOR_BGR2HSV)
            angle90_hsv = cv.cvtColor(frame[192:288,426:640], cv.COLOR_BGR2HSV)
            angle120_hsv = cv.cvtColor(frame[288:384,426:640], cv.COLOR_BGR2HSV)
            angle150_hsv = cv.cvtColor(frame[384:480,426:640], cv.COLOR_BGR2HSV)
            angle0_hsv = cv.cvtColor(frame[0:160,213:426], cv.COLOR_BGR2HSV)
            angle180_hsv = cv.cvtColor(frame[320:480,213:426], cv.COLOR_BGR2HSV)
            angle210_hsv = cv.cvtColor(frame[384:480,0:213], cv.COLOR_BGR2HSV)
            angle240_hsv = cv.cvtColor(frame[288:384,0:213], cv.COLOR_BGR2HSV) 
            angle270_hsv = cv.cvtColor(frame[192:288,0:213], cv.COLOR_BGR2HSV)
            angle300_hsv = cv.cvtColor(frame[96:192,0:213], cv.COLOR_BGR2HSV)
            angle330_hsv = cv.cvtColor(frame[0:96,0:213], cv.COLOR_BGR2HSV)                 

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

            angle = weaponAngle(angle30_mask,0,96,426,640,self.angle)
            angle = weaponAngle(angle60_mask,96,192,426,640,angle)
            angle = weaponAngle(angle90_mask,192,288,426,640,angle)
            angle = weaponAngle(angle120_mask,288,384,426,640,angle)
            angle = weaponAngle(angle150_mask,384,480,426,640,angle)
            angle = weaponAngle(angle0_mask,0,160,213,426,angle)
            angle = weaponAngle(angle180_mask,320,480,213,426,angle)
            angle = weaponAngle(angle210_mask,384,480,0,213,angle)
            angle = weaponAngle(angle240_mask,288,384,0,213,angle)
            angle = weaponAngle(angle270_mask,192,288,0,213,angle)
            angle = weaponAngle(angle300_mask,96,192,0,213,angle)
            angle = weaponAngle(angle330_mask,0,96,0,213,angle)

            self.angle = angle

        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        position = self.weapon.player.hitbox.center
        if weapon:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.image, self.angle, 1)
        else:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)

        offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + offset_rotated)
        self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)
        self.offset_rotated = Vector2(0, -35).rotate(-self.angle)

    def swing(self):
        self.angle += 20 * self.swing_side
        position = self.weapon.player.hitbox.center
        self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)
        offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + offset_rotated)
        # self.rect_mask = get_mask_rect(self.image, *self.rect.topleft)
        self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)
        self.counter += 1

#Weapon Interaction
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
        if self.game.player.hitbox.colliderect(self.rect):
            self.image = self.image_picked
            self.interaction = True
        else:
            self.image = self.original_image
            self.interaction = False
            self.show_name.reset_line_length()

    def interact(self):
        self.weapon_swing.reset()
        self.player = self.game.player
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
                self.game.player.weapon.special_effect(enemy)
                enemy.hurt = True
                enemy.hp -= self.game.player.weapon.damage * self.game.player.strength
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

#Weapon Types
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
        elif 0 > self.weapon_swing.angle > -90:
            self.firing_position = self.hitbox.topright
        else:
            self.firing_position = (self.hitbox.bottomright[0], self.hitbox.bottomright[1] - 15)

    def fire(self):
        pos = pygame.mouse.get_pos()
        self.update_hitbox()
        self.calculate_firing_position()
        self.game.bullet_manager.add_bullet(
            StaffBullet(self.game, self, self.game.world_manager.current_room, self.firing_position[0],
                        self.firing_position[1], pos))
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

    def screen_shake(self):
        self.game.screen_position = (random.randint(-3, 3), random.randint(-3, 3))

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
            self.screen_shake()
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
