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
from .speech import Speech

world_size = (20* 64, 12*64)
host = '192.168.137.1'
port = 12347

def process_inputs(ECE180_input, speech):
    pressed = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    last_e_press = 0
    if pressed[pygame.K_w]:
        ECE180_input["gesture"] = 1
    elif pressed[pygame.K_w] and pressed[pygame.K_a]:
        ECE180_input["gesture"] = 2
    elif pressed[pygame.K_a]:
        ECE180_input["gesture"] = 3
    elif pressed[pygame.K_s] and pressed[pygame.K_a]:
        ECE180_input["gesture"] = 4
    elif pressed[pygame.K_s]:
        ECE180_input["gesture"] = 5
    elif pressed[pygame.K_s] and pressed[pygame.K_d]:
        ECE180_input["gesture"] = 6
    elif pressed[pygame.K_d]:
        ECE180_input["gesture"] = 7
    elif pressed[pygame.K_d] and pressed[pygame.K_w]:
        ECE180_input["gesture"] = 8
    elif pressed[pygame.K_e] and not speech.listening and (current_time - last_e_press > 300):
        last_e_press = current_time
        speech.toggle_listening(ECE180_input)
    return ECE180_input

def callback_speech(list, ECE180_input, command):
    if command in list["pick up"]:
        ECE180_input["speech"] = "pick up"
    elif command in list["drop it"]:
        ECE180_input["speech"] = "drop it"
    else:
        ECE180_input["speech"] = " "

def main():
    screen = pygame.display.set_mode(world_size)

    clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))

    ECE180_input = {
        "gesture": 0,
        "speech": " "
    }

    speech = Speech(callback=callback_speech)

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

        ECE180_input = process_inputs(ECE180_input, speech)
        input = pickle.dumps(ECE180_input)
        clientsocket.send(input)

        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ =="__main__":
    main()
