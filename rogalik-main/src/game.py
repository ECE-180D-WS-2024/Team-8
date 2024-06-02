import pygame
import paho.mqtt.client as mqtt
import random

from .entities.enemy_manager import EnemyManager
from .entities.player import Player

from .entities.player2 import Player2
from .entities.enemy import Imp
from .menu import MainMenu
from .mini_map import MiniMap
from .particles import ParticleManager
from .hud import Hud
from .background import BackgroundEffects
from .map.world_manager import WorldManager
from .objects.object_manager import ObjectManager
from .game_over import GameOver
import time
from .bullet import BulletManager
from .sound_manager import SoundManager
from .tutorial import Tutorial
import socket
import pickle
import sys
import threading
import select
import io
import base64
import zlib
import gzip
import struct

pygame.init()
pygame.mixer.init()

world_size = (20*64, 12*64)
ip_address = '172.26.235.77'

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(world_size)
        self.screen = pygame.Surface(world_size).convert()
        self.clock = pygame.time.Clock()
        self.enemy_manager = EnemyManager(self)
        self.particle_manager = ParticleManager(self)
        self.world_manager = WorldManager(self)
        self.object_manager = ObjectManager(self)
        self.bullet_manager = BulletManager(self)
        self.sound_manager = SoundManager(self)
        self.player = Player(self)
        self.player2 = Player2(self)
        self.hud1 = Hud(self, "player")
        self.hud2 = Hud(self, "player2")
        self.tutorial = Tutorial(self)
        self.running = True
        self.menu = MainMenu(self)
        self.mini_map = MiniMap(self)
        self.game_time = None
        self.state_num = 0
        self.last_j_press = 0
        white = (255, 255, 255)
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = font.render('Move to weapon', True, white)
        self.TutorialText = self.text.get_rect()
        self.TutorialText.center= (805,60)
        self.tutorial_enemy_spawned = False
        
        self.fps = 30
        #self.background = BackgroundEffects()
        self.game_over = GameOver(self)
        pygame.mixer.init()
        self.dt = 0
        self.inputs = {"gesture": 0,
                       "speech": " ",
                       "localization": 0}

        self.sound = pygame.mixer.Sound('./assets/sound/dungeon_theme_1.wav')
        self.screen_position = (0, 0)

    def refresh(self):
        pygame.mixer.Sound.stop(self.sound)
        self.__init__()
        pygame.display.flip()
        self.run_game()

    def update_groups(self):
        self.enemy_manager.update_enemies()
        self.object_manager.update()
        self.player.update()
        self.player2.update()
        self.particle_manager.update_particles()
        self.particle_manager.update_fire_particles()
        self.bullet_manager.update()
        #self.background.update()
        self.world_manager.update()
        self.game_over.update()
        self.mini_map.update()

    def draw_groups(self):
        self.world_manager.draw_map(self.screen)
        if self.player:
            self.player.draw(self.screen)
        if self.player2:
            self.player2.draw(self.screen)
        self.enemy_manager.draw_enemies(self.screen)
        self.object_manager.draw()
        self.bullet_manager.draw()
        self.mini_map.draw(self.screen)
        self.hud1.draw()
        self.hud2.draw()
        self.particle_manager.draw_particles(self.world_manager.current_map.map_surface)
        #self.particle_manager.draw_fire_particles()
        self.game_over.draw()

    def input(self):

        white = (255, 255, 255)
        font = pygame.font.Font('freesansbold.ttf', 16)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.USEREVENT:
                self.object_manager.up += 1
                self.object_manager.hover = True
        self.player2.input()
        self.player.input()
        pressed = pygame.key.get_pressed()
        if(self.state_num < 5):
            if pressed[pygame.K_j] and ((current_time - self.last_j_press) > 300):
                self.last_j_press = current_time
                self.state_num = self.state_num + 1
            if pressed[pygame.K_k] and (self.state_num > 0):
                self.state_num = self.state_num - 1
            if(self.state_num == 0):
                self.text = font.render('I am the Rogue Master and welcome to the dungeon. Before you begin exploring these dungeons, I wil have to prepare you to be a warrior. Press J to go next.', True, white)
            elif(self.state_num == 1):
                self.text = font.render('First, you must learn how to move. Your character can be controlled with the avatar controller. Tilt it forward to move and rotate your controller in the direction you would like to go. Navigate to the weapon. Press J to go next or K to go back.', True, white)
            elif(self.state_num == 2):
                self.text = font.render('Now that you are hovering the weapon, you can use the magic button on your wand to activate your voice commands. After pressing the button, say Pick it up to obtain your weapon. Press J to go next or K to go back.', True, white)
            elif(self.state_num == 3):
                self.text = font.render('You can control your weapon by orienting the end of your magic wand in front of the camera in the position you want. The magical powers will then control the weapon on your screen. After you\'re done trying out the weapon, press J to spawn a monster to test what you\'ve learned!', True, white)
            elif(self.state_num == 4):
                self.text = font.render('Fight the enemy with your magic wand and avatar controller! After the monster is defeated, you can now go to the next rooms! Happy exploring. Press J to end tutorial.', True, white)
                if not self.tutorial_enemy_spawned:
                    self.world_manager.world.starting_room.enemy_list.append(Imp(self, random.randint(100, 150) / 10, 50, self.world_manager.world.starting_room))
                    self.world_manager.world.starting_room.enemy_list[-1].damage = 0
                    self.enemy_manager.upgrade_enemy(self.world_manager.world.starting_room.enemy_list[-1])
                    self.world_manager.world.starting_room.enemy_list[-1].spawn()
                    print(len(self.world_manager.world.starting_room.enemy_list))
                self.tutorial_enemy_spawned = True
            self.TutorialText = self.text.get_rect()
            self.TutorialText.center= (805,60)
            self.screen.blit(self.text, self.TutorialText)
        if pressed[pygame.K_ESCAPE]:
            if self.game_over.game_over:
                self.refresh()
            self.menu.running = True
            self.menu.play_button.clicked = False

    def run_game(self):
        counter = 0
        white = (255, 255, 255)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text1 = font.render('Waiting for the second player', True, white)
        text2 = font.render("Your IP Address is " + ip_address, True, white)
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()

        #print(self.player2.speech.message)
        font_speech = './assets/font/Minecraft.ttf'
        pygame.font.init()
        font = pygame.font.Font(font_speech, 15)
        speech_text1 = font.render(self.player2.speech.message, True, white)
        speech_textRect1 = speech_text1.get_rect(topleft=(320, 60))

        speech_text2 = font.render('Pick Up/Drop It', True, white)
        speech_textRect2 = speech_text2.get_rect(topleft=(320, 75))

        textRect1.center = (20*64 // 2, 12*64 // 2)
        textRect2.center = (20*64 // 2, 12*64 // 2 - 100)
            
        self.enemy_manager.add_enemies()
        prev_time = time.time() 
        pygame.mixer.Sound.play(self.sound, loops=-1)
        while self.running:
            self.clock.tick(self.fps)
            now = time.time()
            self.dt = now - prev_time
            prev_time = now
            self.menu.show()
            if (self.menu.running == False and counter == 0):
                host = ip_address
                port = 12347
                server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                server.bind((host, port))
                server.listen()
                server.settimeout(1.0)
                while True:
                    self.screen.fill((0, 0, 0))
                    self.display.blit(self.screen, self.screen_position)
                    self.display.blit(text1, textRect1)
                    self.display.blit(text2, textRect2)
                    pygame.display.flip()
                    try:
                        client, address = server.accept()
                        if(client):
                            break
                    except socket.timeout:
                        continue
                counter = counter + 1

            self.screen.fill((0, 0, 0))
            self.input()
            self.update_groups()
            self.draw_groups()
            self.game_time = pygame.time.get_ticks()
            data = pygame.image.tobytes(self.screen, "RGB")
            data = zlib.compress(data)
            size = len(data)
            # Prefix the image data with its size
            size_data = struct.pack("!I", size)
            client.sendall(size_data)
            client.sendall(data)
            self.display.blit(self.screen, self.screen_position)
            self.display.blit(speech_text1, speech_textRect1)
            self.display.blit(speech_text2, speech_textRect2)
            client.recv(1)
            input_data = client.recv(1024)
            self.inputs = pickle.loads(input_data)
            if(self.player2.speech.reset != " "):
                self.player2.speech.message = "Press E and say:"
            self.player2.speech.reset = " "

            #print(self.inputs)
            if self.running:
                pygame.display.flip()
        self.client.loop_stop()
        self.client.disconnect()
        pygame.quit()
