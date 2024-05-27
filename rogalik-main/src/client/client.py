import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
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
import paho.mqtt.client as mqtt
from speech import Speech



class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.counter = 0  # Use a class attribute instead of a global variable
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("lol123")

    def on_message(self, client, userdata, msg):
        try:
            # Attempt to convert the message payload to an integer
            self.counter = int(msg.payload)

        except ValueError:
            dummy = 0

    def connect(self):
        self.client.connect_async('mqtt.eclipseprojects.io')
        self.client.loop_start()

    def counter(self):
        return self._counter


pygame.init()

world_size = (20* 64, 12*64)
ip_address = '172.20.2.35'
host = ip_address
port = 12347
white = (255, 255, 255)
active = False

cap = cv.VideoCapture(0)
#img_mask = your target detected mask of frame; X's Y's are the coordinate of your target frame
def weaponAngle(img_mask,y1,y2,x1,x2,pre_angle):
    angle = pre_angle
    area = 0
    attackArea = 100
    contours,hierarchy = cv.findContours(img_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt) 
        #Try increase the sensitivity by increase the diversity of angle (orientation) 180/6=30
        if(area > attackArea):
            if(x1 == 0 and x2 == 250 and y1 == 0 and y2 == 43):
                angle = 1 #(345)
            if(x1 == 0 and x2 == 250 and y1 == 43 and y2 == 86):
                angle = 2 #(330)
            if(x1 == 0 and x2 == 250 and y1 == 86 and y2 == 129):
                angle = 3 #(315)
            if(x1 == 0 and x2 == 250 and y1 == 129 and y2 == 172):
                angle = 4 #(300)
            if(x1 == 0 and x2 == 250 and y1 == 172 and y2 == 215):
                angle = 5 #(285)
            if(x1 == 0 and x2 == 250 and y1 == 215 and y2 == 258):
                angle = 6 #(270)
            if(x1 == 0 and x2 == 250 and y1 == 258 and y2 == 301):
                angle = 7 #(255)
            if(x1 == 0 and x2 == 250 and y1 == 301 and y2 == 344):
                angle = 8 #(240)
            if(x1 == 0 and x2 == 250 and y1 == 344 and y2 == 387):
                angle = 9 #225
            if(x1 == 0 and x2 == 250 and y1 == 387 and y2 == 430):
                angle = 10 #210
            if(x1 == 0 and x2 == 250 and y1 == 430 and y2 == 480):
                angle = 11 #195
            if(x1 == 250 and x2 == 390 and y1 == 240 and y2 == 480):
                angle = 12 #180
            if(x1 == 250 and x2 == 390 and y1 == 0 and y2 == 240):
                angle = 13 #0
            if(x1 == 390 and x2 == 640 and y1 == 0 and y2 == 43):
                angle = 14 #15
            if(x1 == 390 and x2 == 640 and y1 == 43 and y2 == 86):
                angle = 15 #30
            if(x1 == 390 and x2 == 640 and y1 == 86 and y2 == 129):
                angle = 16 #45
            if(x1 == 390 and x2 == 640 and y1 == 129 and y2 == 172):
                angle = 17 #60
            if(x1 == 390 and x2 == 640 and y1 == 172 and y2 == 215):
                angle = 18 #75
            if(x1 == 390 and x2 == 640 and y1 == 215 and y2 == 258):
                angle = 19 #90
            if(x1 == 390 and x2 == 640 and y1 == 258 and y2 == 301):
                angle = 20 #105
            if(x1 == 390 and x2 == 640 and y1 == 301 and y2 == 344):
                angle = 21 #120
            if(x1 == 390 and x2 == 640 and y1 == 344 and y2 == 387):
                angle = 22 #135
            if(x1 == 390 and x2 == 640 and y1 == 387 and y2 == 430):
                angle = 23 #150
            if(x1 == 390 and x2 == 640 and y1 == 430 and y2 == 480):
                angle = 24 #165
        else:
            angle = 25

    return angle

def process_inputs(ECE180_input, current_time, last_e_press, message):
    pressed = pygame.key.get_pressed()
    speech = Speech(callback=callback_speech)
    if pressed[pygame.K_e] and not speech.listening and (current_time - last_e_press > 300):
        last_e_press = current_time
        speech.toggle_listening(ECE180_input, message)
    message = message
 

    return ECE180_input, message

def callback_speech(list, ECE180_input, command, message):
    if command in list["pick up"]:
        ECE180_input["speech"] = "pick up"
    elif command in list["drop it"]:
        ECE180_input["speech"] = "drop it"

def main():
    global active
    font = pygame.font.Font('freesansbold.ttf', 16)
    screen = pygame.display.set_mode(world_size)
    temp_screen1 = pygame.display.set_mode(world_size)
    temp_screen2 = pygame.display.set_mode(world_size)
    temp_screen3 = pygame.display.set_mode(world_size)
    
    mqtt_client = MQTTClient()

#GUI For IP address confirmation ---------------------------------
    input_text = ''
    white = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    text1 = font.render('Please enter your IP Address:', True, white)
    text2 = font.render('Your IP address is correct', True, white)
    text4 = font.render('Connecting to the main server.....', True, white)
    text3 = font.render('Your IP address is wrong', True, white)
    
    textRect1 = text1.get_rect()
    textRect1.center = (20*64 // 2 - 100, 12*64 // 2)
    textRect2 = text2.get_rect()
    textRect2.center = (20*64 // 2, 12*64 // 2 - 100)
    textRect3 = text3.get_rect()
    textRect3.center = (20*64 // 2, 12*64 // 2)
    textRect4 = text4.get_rect()
    textRect4.center = (20*64 // 2, 12*64 // 2 + 100)
    input_rect = pygame.Rect(785, 365, 140, 32) #(x,y, boxsize of x, boxsize of y)
    
    IP_GUI = True
    while(IP_GUI):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN: 
                if active == True:
                    if event.key == pygame.K_BACKSPACE: 
                        input_text = input_text[:-1] 
                        print("K_backspace")
                    elif event.key == pygame.K_RETURN:
                        print("K_enter")
                        if(ip_address == input_text):    
                            screen2_count = 0
                            screen2_stop = 100
                            while(screen2_count <= screen2_stop):
                                temp_screen2.fill((0,0,0))
                                temp_screen2.blit(text2, textRect2)
                                temp_screen2.blit(text4, textRect4)
                                screen2_count = screen2_count + 0.01
                                pygame.display.flip()
                            IP_GUI = False
                        elif(ip_address != input_text):
                            screen3_count = 0
                            screen3_stop = 20
                            while(screen3_count <= screen3_stop):
                                temp_screen3.fill((0,0,0))
                                temp_screen3.blit(text3, textRect3)
                                screen3_count = screen3_count + 0.01
                                pygame.display.flip()
                    else: 
                        input_text += event.unicode
                        print(input_text)

        if(IP_GUI == True):
            temp_screen1.fill((0,0,0))
            #pygame.draw.rect(temp_screen1,white,input_rect,2)
            input_surface = font.render(input_text, True, (255, 255, 255)) 
            temp_screen1.blit(text1, textRect1)
            temp_screen1.blit(input_surface, (input_rect.x+5, input_rect.y+5)) 
            input_rect.w = max(100, input_surface.get_width()+10) 

            pygame.display.flip()
#GUI For IP address confirmation ---------------------------------
    mqtt_client.connect()
    clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))
    #Localization
    # define range of blue color in HSV
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([40,255,255]) 
    lower_green = np.array([65,100,100])
    upper_green = np.array([85,255,255])
    lower_blue = np.array([110,255,255])
    upper_blue = np.array([130,255,255])

    lower_color = lower_yellow
    upper_color = upper_yellow
    pre_angle = 0
    #---------------------------------------------
    last_e_press = 0
    # loop .recv, it returns empty string when done, then transmitted data is completely received
    ECE180_input = {
            "gesture": 0,
            "speech": " ",
            "localization": 0,
    }   
    message = {
            "1": "Press E & say: pick up/drop it"
    }

    while True:
        
        text = font.render(message["1"], True, white)
        textRect = text.get_rect()
        textRect.center = (805, 60)
        current_time = pygame.time.get_ticks()
        # print(current_time)
        _,frame = cap.read()
        #--------
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

        angle = weaponAngle(angle15_mask,0,43,390,640,pre_angle)
        angle = weaponAngle(angle30_mask,43,86,390,640,angle)
        angle = weaponAngle(angle45_mask,86,129,390,640,angle)
        angle = weaponAngle(angle60_mask,129,172,390,640,angle)
        angle = weaponAngle(angle75_mask,172,215,390,640,angle)
        angle = weaponAngle(angle90_mask,215,258,390,640,angle)
        angle = weaponAngle(angle105_mask,258,301,390,640,angle)
        angle = weaponAngle(angle120_mask,301,344,390,640,angle)
        angle = weaponAngle(angle135_mask,344,387,390,640,angle)
        angle = weaponAngle(angle150_mask,430,480,390,640,angle)
        angle = weaponAngle(angle165_mask,430,480,390,640,angle)
        angle = weaponAngle(angle0_mask,0,240,250,390,angle)
        angle = weaponAngle(angle180_mask,240,480,0,250,angle)
        angle = weaponAngle(angle195_mask,430,480,0,250,angle)
        angle = weaponAngle(angle210_mask,387,430,0,250,angle)
        angle = weaponAngle(angle225_mask,344,387,0,250,angle)
        angle = weaponAngle(angle240_mask,301,344,0,250,angle)
        angle = weaponAngle(angle255_mask,258,301,0,250,angle)
        angle = weaponAngle(angle270_mask,215,258,0,250,angle)
        angle = weaponAngle(angle285_mask,172,215,0,250,angle)
        angle = weaponAngle(angle300_mask,129,172,0,250,angle)
        angle = weaponAngle(angle315_mask,86,129,0,250,angle)
        angle = weaponAngle(angle330_mask,43,86,0,250,angle)
        angle = weaponAngle(angle345_mask,0,43,0,250,angle)             
    
        pre_angle = angle   
        ECE180_input['localization'] = angle
        ECE180_input["gesture"] = mqtt_client.counter
  
        size_data = clientsocket.recv(4)
        size = struct.unpack("!I", size_data)[0]
        data = b''
        while len(data) < size:
            r_data = clientsocket.recv(3949120)
            data += r_data

        data = zlib.decompress(data)
        image = pygame.image.frombytes(data, world_size, "RGB")
        screen.blit(image,(0,0)) # "show image" on the screen
        screen.blit(text, textRect)
        pygame.display.flip()
        clientsocket.send(b'1')

        ECE180_input, message = process_inputs(ECE180_input,current_time, last_e_press, message)
        if(ECE180_input["speech"] != " "):
            message["1"] = "Press E & say: pick up/drop it"
        input = pickle.dumps(ECE180_input)
        clientsocket.send(input)
        ECE180_input["speech"] = " "
        
        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ =="__main__":
    main()
