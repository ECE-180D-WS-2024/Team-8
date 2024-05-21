import pygame
import paho.mqtt.client as mqtt

from .entities.enemy_manager import EnemyManager
from .entities.player import Player

from .entities.player2 import Player2

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

        self.running = True
        self.menu = MainMenu(self)
        self.mini_map = MiniMap(self)
        self.game_time = None

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.USEREVENT:
                self.object_manager.up += 1
                self.object_manager.hover = True
        self.player2.input()
        self.player.input()
        pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_r]:
        #     self.refresh()

        if pressed[pygame.K_ESCAPE]:
            if self.game_over.game_over:
                self.refresh()
            self.menu.running = True
            self.menu.play_button.clicked = False

    def run_game(self):
        counter = 0
        white = (255, 255, 255)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Waiting for the second player', True, white)
        textRect = text.get_rect()
        textRect.center = (20*64 // 2, 12*64 // 2)
            
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
                host = '172.26.235.9'
                port = 12347
                server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                server.bind((host, port))
                server.listen()
                server.settimeout(1.0)
                while True:
                    self.screen.fill((0, 0, 0))
                    self.display.blit(self.screen, self.screen_position)
                    self.display.blit(text, textRect)
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
            client.recv(1)
            input_data = client.recv(1024)
            self.inputs = pickle.loads(input_data)
            #print(self.inputs)
            if self.running:
                pygame.display.flip()
        self.client.loop_stop()
        self.client.disconnect()
        pygame.quit()
