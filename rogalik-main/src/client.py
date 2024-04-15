import socket
import pygame
import sys
import io
import base64
import pickle
import zlib
import select
import gzip
import struct
world_size = (20* 64, 12*64)
host = '192.168.137.1'
port = 12347
screen = pygame.display.set_mode(world_size)

clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))
received = []
ack = 0
# loop .recv, it returns empty string when done, then transmitted data is completely received
while True:
    size_data = clientsocket.recv(4)
    size = struct.unpack("!I", size_data)[0]
    data = b''
    while len(data) < size:
        r_data = clientsocket.recv(3949120)
        data += r_data

    data = zlib.decompress(data)
    image = pygame.image.frombytes(data, world_size, "RGB")
    screen.blit(image,(0,0)) # "show image" on the screen
    pygame.display.flip()
    clientsocket.send(b'1')

     # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
