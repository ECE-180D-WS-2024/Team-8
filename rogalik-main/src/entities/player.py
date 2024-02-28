#OpenCV
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Pygame
import pygame
from math import sqrt
from src.objects.p import Poop
from src.objects.flask import GreenFlask
from .entity import Entity
from src.particles import Dust

cap = cv.VideoCapture(0)
#img_mask = your target detected mask of frame; X's Y's are the coordinate of your target frame
def AttackDetection(img_mask,pre_attack):
    detectArea = 1000
    attack = pre_attack
    contours,hierarchy = cv.findContours(img_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt) 
        if(area > detectArea):
            attack = True
    return attack

class Player(Entity):
    name = 'player'
    speed = 360
    max_hp = 100
    gold = 0
    shield = 1
    strength = 1
    hp = max_hp
    items = []

    def __init__(self, game):
        Entity.__init__(self, game, self.name)
        self.rect = self.image.get_rect(center=(512 + 2.5 * 64, 600))
        self.weapon = None
        self.attacking = False
        self.interaction = True
        self.attack_cooldown = 350  # ms
        self.room = None
        self.death_counter = 1
        self.falling = False
        self.floor_value = self.rect.y
        self.fall(-100)

    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.direction = 'up'
        if pressed[pygame.K_s]:
            self.direction = 'down'
        if pressed[pygame.K_a]:
            self.direction = 'left'
        if pressed[pygame.K_d]:
            self.direction = 'right'
        if pressed[pygame.K_e] and pygame.time.get_ticks() - self.time > 300:
            self.time = pygame.time.get_ticks()
            self.game.object_manager.interact()
        if pressed[pygame.K_q] and self.weapon and pygame.time.get_ticks() - self.time > 300:
            self.time = pygame.time.get_ticks()
            self.weapon.drop()
            if self.items:
                self.weapon = self.items[0]
        if pressed[pygame.K_TAB]:
            self.game.mini_map.draw_all(self.game.screen)
            self.game.mini_map.draw_mini_map = False
        else:
            self.game.mini_map.draw_mini_map = True
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.items:
                if event.button == 4:
                    self.weapon = self.items[self.items.index(self.weapon) - 1]
                    self.shift_items_left()
                    self.weapon = self.items[0]
                elif event.button == 5:
                    self.weapon = self.items[(self.items.index(self.weapon) + 1) % len(self.items)]
                    self.shift_items_right()
                    self.weapon = self.items[0]

        # constant_dt = 0.06
        constant_dt = self.game.dt
        vel_up = [0, -self.speed * constant_dt]
        vel_up = [i * pressed[pygame.K_w] for i in vel_up]
        vel_down = [0, self.speed * constant_dt]
        vel_down = [i * pressed[pygame.K_s] for i in vel_down]
        vel_left = [-self.speed * constant_dt, 0]
        vel_left = [i * pressed[pygame.K_a] for i in vel_left]
        vel_right = [self.speed * constant_dt, 0]
        vel_right = [i * pressed[pygame.K_d] for i in vel_right]
        vel = zip(vel_up, vel_down, vel_left, vel_right)
        vel_list = [sum(item) for item in vel]

        x = sqrt(pow(vel_list[0], 2) + pow(vel_list[1], 2))

        if 0 not in vel_list:
            z = x / (abs(vel_list[0]) + abs(vel_list[1]))
            vel_list_fixed = [item * z for item in vel_list]
            self.set_velocity(vel_list_fixed)
        else:
            self.set_velocity(vel_list)

        #Auto Attack
        #----------------------------------------------------------------------------------------------------------------------------------------------
        '''
        attackspeed = 1.5
        k = attackspeed
        if pygame.time.get_ticks() - self.time > k*self.attack_cooldown and self.weapon:
            self.time = pygame.time.get_ticks()
            self.attacking = True
            if self.weapon.name != 'staff':
                self.weapon.weapon_swing.swing_side *= (-1) 
        '''
        #'''
        attackspeed = 1.5
        k = attackspeed
        
        if pygame.time.get_ticks() - self.time > k*self.attack_cooldown and self.weapon:
            self.time = pygame.time.get_ticks()   

            '''     
            lower_yellow = np.array([20,100,100])
            upper_yellow = np.array([40,255,255]) 
            lower_green = np.array([50,100,100])
            upper_green = np.array([70,255,255])

            lower_color = lower_yellow
            upper_color = upper_yellow
            
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

            attack = AttackDetection(angle30_mask,self.attacking)
            attack = AttackDetection(angle60_mask,attack)
            attack = AttackDetection(angle90_mask,attack)
            attack = AttackDetection(angle120_mask,attack)
            attack = AttackDetection(angle150_mask,attack)
            attack = AttackDetection(angle0_mask,attack)
            attack = AttackDetection(angle180_mask,attack)
            attack = AttackDetection(angle210_mask,attack)
            attack = AttackDetection(angle240_mask,attack)
            attack = AttackDetection(angle270_mask,attack)
            attack = AttackDetection(angle300_mask,attack)
            attack = AttackDetection(angle330_mask,attack)

            self.attacking = attack
            '''
            self.attacking = True
            if self.weapon.name != 'staff':
                self.weapon.weapon_swing.swing_side *= (-1)                 
        #'''
        #----------------------------------------------------------------------------------------------------------------------------------------------

    def shift_items_right(self):
        self.items = [self.items[-1]] + self.items[:-1]

    def shift_items_left(self):
        self.items = self.items[1:] + [self.items[0]]

    def falling_update(self):
        if self.rect.y < self.floor_value:
            value = 15
            self.rect.y += value
        else:
            self.falling = False
            self.game.sound_manager.play(pygame.mixer.Sound('./assets/sound/Hit.wav'))

    def add_walking_particles(self):
        if self.moving():
            self.game.sound_manager.play_walk_sound()
            self.game.particle_manager.add_particle(Dust(self.game, self, *self.rect.midbottom))

    def update(self) -> None:
        if self.falling:
            self.falling_update()
        else:
            self.add_walking_particles()
            if self.death_counter == 0:
                return
            self.entity_animation.update()
            self.wall_collision()
            if self.can_move:
                self.rect.move_ip(*self.velocity)
                self.hitbox.move_ip(*self.velocity)
            self.detect_death()
        if self.weapon:
            self.weapon.update()
        self.update_hitbox()

    def fall(self, value):
        self.rect.y = value
        self.falling = True

    def calculate_collision(self, enemy):
        if not self.shield and not self.dead:
            self.hp -= enemy.damage
            self.game.sound_manager.play(self.game.sound_manager.player_hurt)
            if not self.dead:
                self.hurt = True
            self.entity_animation.hurt_timer = pygame.time.get_ticks()
        if self.shield:
            self.shield -= 1
            self.game.sound_manager.play(pygame.mixer.Sound('./assets/sound/Random1.wav'))

    def draw(self, surface):
        if self.death_counter == 0:
            return
        self.draw_shadow(surface)
        surface.blit(self.image, self.rect)
        if self.weapon:
            self.weapon.draw()
