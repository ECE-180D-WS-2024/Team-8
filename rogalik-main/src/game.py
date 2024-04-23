import pygame

from .entities.enemy_manager import EnemyManager
from .entities.player import Player
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
        self.hud = Hud(self)
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
        self.particle_manager.update_particles()
        self.particle_manager.update_fire_particles()
        self.bullet_manager.update()
        #self.background.update()
        self.world_manager.update()
        self.game_over.update()
        self.mini_map.update()

    def draw_groups(self):
        #self.background.draw(self.screen)
        self.world_manager.draw_map(self.screen)
        if self.player:
            self.player.draw(self.screen)
        self.enemy_manager.draw_enemies(self.screen)
        self.object_manager.draw()
        self.bullet_manager.draw()
        self.mini_map.draw(self.screen)
        self.hud.draw()
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
        host = '172.26.193.221'
        port = 12347
        server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        server.settimeout(1.0)  # Allow timeout to process KeyboardInterrupt
        counter = 0
        while True:
            try:
                client, address = server.accept()
                if(client):
                    break
            except socket.timeout:
                continue
            
        self.enemy_manager.add_enemies()
        prev_time = time.time() 
        pygame.mixer.Sound.play(self.sound, loops=-1)
        while self.running:
            self.clock.tick(self.fps)
            now = time.time()
            self.dt = now - prev_time
            prev_time = now
            self.menu.show()
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
            if self.running:
                pygame.display.flip()
        pygame.quit()
