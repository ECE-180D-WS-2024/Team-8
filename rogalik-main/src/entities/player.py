import pygame
from math import sqrt
from src.objects.p import Poop
from src.objects.flask import GreenFlask
from .entity import Entity
from src.particles import Dust

pygame.init()
def recovery(client_angle):
    angle = 0
    attack_area = 0
    if(client_angle == 1):
        angle = 345
        attack_area = 1
    elif(client_angle == 2):
        angle = 330
        attack_area = 1
    elif(client_angle == 3):
        angle = 315  
        attack_area = 1  
    elif(client_angle == 4):
        angle = 300
        attack_area = 1
    elif(client_angle == 5):
        angle = 285  
        attack_area = 1  
    elif(client_angle == 6):
        angle = 270  
        attack_area = 1  
    elif(client_angle == 7):
        angle = 255
        attack_area = 1
    elif(client_angle == 8):
        angle = 240 
        attack_area = 1   
    elif(client_angle == 9):
        angle = 225   
        attack_area = 1 
    elif(client_angle == 10):
        angle = 210
        attack_area = 1
    elif(client_angle == 11):
        angle = 195 
        attack_area = 1   
    elif(client_angle == 12):
        angle = 180  
        attack_area = 1  
    elif(client_angle == 13):
        angle = 0
        attack_area = 1
    elif(client_angle == 14):
        angle = 15 
        attack_area = 1   
    elif(client_angle == 15):
        angle = 30  
        attack_area = 1  
    elif(client_angle == 16): 
        angle = 45
        attack_area = 1
    elif(client_angle == 17):
        angle = 60
        attack_area = 1
    elif(client_angle == 18):
        angle = 75 
        attack_area = 1
    elif(client_angle == 19):
        angle = 90
        attack_area = 1
    elif(client_angle == 20):
        angle = 105
        attack_area = 1
    elif(client_angle == 21):
        angle = 120
        attack_area = 1
    elif(client_angle == 22):
        angle = 135
        attack_area = 1
    elif(client_angle == 23):  
        angle = 150
        attack_area = 1
    elif(client_angle == 24):      
        angle = 165
        attack_area = 1
    elif(client_angle == 25):
        attack_area = 0
    
    return attack_area,angle

class Player(Entity):
    name = 'player'
    speed = 200
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
        self.keydeterm = {"K_w":False, "K_s":False, "K_a":False, "K_d":False}

    def input(self):
        pressed = pygame.key.get_pressed()
        
        self.keydeterm = {"K_w":False, "K_s":False, "K_a":False, "K_d":False}
        if self.game.inputs["gesture"] == 1 or self.game.inputs["gesture"] == 2 or self.game.inputs["gesture"] == 8:
            self.keydeterm["K_w"] = True
        if self.game.inputs["gesture"] == 4 or self.game.inputs["gesture"] == 5 or self.game.inputs["gesture"] == 6:
            self.keydeterm["K_s"] = True
        if self.game.inputs["gesture"] == 2 or self.game.inputs["gesture"] == 3 or self.game.inputs["gesture"] == 4:
            self.keydeterm["K_a"] = True
        if self.game.inputs["gesture"] == 6 or self.game.inputs["gesture"] == 7 or self.game.inputs["gesture"] == 8:
            self.keydeterm["K_d"] = True

        if self.keydeterm["K_w"]:
            self.direction = 'up'
        if self.keydeterm["K_s"]:
            self.direction = 'down'
        if self.keydeterm["K_a"]:
            self.direction = 'left'
        if self.keydeterm["K_d"]:
            self.direction = 'right'

        if self.game.inputs["speech"] != " " and self.game.inputs["speech"] == "pick up":
            self.game.object_manager.interact(self.name)
        if self.game.inputs["speech"] == "drop it" and self.weapon:
            self.weapon.drop()
            if self.items:
                self.weapon = self.items[0]
        if pressed[pygame.K_TAB]:
            self.game.mini_map.draw_all(self.game.screen)
            self.game.mini_map.draw_mini_map = False
        else:
            self.game.mini_map.draw_mini_map = True
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN and self.items:
        #         if event.button == 4:
        #             self.weapon = self.items[self.items.index(self.weapon) - 1]
        #             self.shift_items_left()
        #             self.weapon = self.items[0]
        #         elif event.button == 5:
        #             self.weapon = self.items[(self.items.index(self.weapon) + 1) % len(self.items)]
        #             self.shift_items_right()
        #             self.weapon = self.items[0]

        constant_dt = self.game.dt
        vel_up = [0, -self.speed * constant_dt]
        vel_up = [i * self.keydeterm["K_w"] for i in vel_up]
        vel_down = [0, self.speed * constant_dt]
        vel_down = [i * self.keydeterm["K_s"] for i in vel_down]
        vel_left = [-self.speed * constant_dt, 0]
        vel_left = [i * self.keydeterm["K_a"] for i in vel_left]
        vel_right = [self.speed * constant_dt, 0]
        vel_right = [i * self.keydeterm["K_d"] for i in vel_right]
        vel = zip(vel_up, vel_down, vel_left, vel_right)
        vel_list = [sum(item) for item in vel]

        x = sqrt(pow(vel_list[0], 2) + pow(vel_list[1], 2))

        if 0 not in vel_list:
            z = x / (abs(vel_list[0]) + abs(vel_list[1]))
            vel_list_fixed = [item * z for item in vel_list]
            self.set_velocity(vel_list_fixed)
        else:
            self.set_velocity(vel_list)

#Localizaion ---------------
        if(self.weapon):
            attack_area,angle = recovery(self.game.inputs["localization"])
            attackspeed = 1.7
            if pygame.time.get_ticks() - self.time > attackspeed*self.attack_cooldown and self.weapon:
                self.time = pygame.time.get_ticks()  
                if(attack_area == 1):
                    self.attacking = True
                    self.weapon.weapon_swing.angle = angle
                else:
                    self.attacking = False

                if self.weapon.name != 'staff':
                    self.weapon.weapon_swing.swing_side *= (-1)


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
