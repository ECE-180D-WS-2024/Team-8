import pygame
import threading
import speech_recognition as sr

class Speech:
    def __init__(self, callback=None):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.callback = callback
        self.listening = False
        self.thread = None
        self.stop_event = threading.Event()
        self.last_command = None
        self.command_alternatives = {
            "pick up": ["pick up", "wake up", "pickup", "wakeup", "pick it up", "can you pick it up", "pick that up", "panda" ],
            "drop it": ["drop", "drop it", "dropit", "stopit", "stop it", "dropp it", "droppit", "trumpet" ]
            #add more here
        }
        self.show_status = ""
    
    # def show_speech(self, message):
    #     self.show_status = message
    #     if self.callback:
    #         self.callback(message)

    def _listen(self, ECE180_input, message):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                #self.show_speech("Say Command")
                print("Say Command")
                message["1"] = "Say Command"
                audio = self.recognizer.listen(source, timeout=2.5, phrase_time_limit=1)
                #duration
                command = self.recognizer.recognize_google(audio).lower()
                #self.show_speech(f"Recognized: {command}")
                print(f"Recognized: {command}")
                if self.process_command(command):
                    #print("speech command recognized")
                    if self.callback:
                        self.callback(self.command_alternatives, ECE180_input,command, message)
                else:
                    print("Recognition Failed. Cast purple to try again.")
                    message["1"] = "Cast Purple to Try Again"
            except sr.RequestError as e:
                # Handle request error, log, or retry logic
                #self.show_speech(f"API unavailable, {e}")
                print(f"API unavailable, {e}")
                message["1"] = "Cast Purple to Try Again"
            except sr.UnknownValueError as e:
                # Handle unknown value error, log, or retry logic
                #self.show_speech(f"Could not understand audio {e}")
                print(f"Could not understand audio {e}")
                message["1"] = "Cast Purple to Try Again"
            except Exception as e:
                #self.show_speech(f"An unexpected error occurred: {e}")
                print(f"An unexpected error occurred: {e}")
                message["1"] = "Cast Purple to Try Again"
        self.listening = False
        self.stop_event.set()
        if self.listening == False:
            print("Thread Stopped")
    #     time.sleep(1)

    def toggle_listening(self, ECE180_input, message):
        """Toggle the listening state and manage the listening thread accordingly."""
        if not self.listening:
            #self.show_speech("Please wait for speech recognition...")
            print("Please wait for speech recognition...")
            self.listening = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._listen, args=(ECE180_input,message))
            self.thread.start()
        else:
            #self.show_speech("Stopping speech recognition thread...")
            print("Stopping speech recognition thread...")
            self.listening = False
            self.stop_event.set()
            self.thread.join()
            self.thread = None
    
    def process_command(self, command):
        # check to see if the command is a key in word bank
        for primary_command, alternatives in self.command_alternatives.items():
            if command in alternatives:
                self.last_command = primary_command
                return True
        return False
    
    def show_command(self, command, screen, position):
        """Display the recognized speech command on the game screen."""
        font = pygame.font.Font(None, 24)  # Use the desired font and size
        text_surface = font.render(command, True, (255, 255, 255))  # White color
        screen.blit(text_surface, position)
    
    # def pickup_command(self, command):
    #     if command == "pick up":
    #         self.last_command = command
    #         return True
    #     return False
    
    def get_last_command(self):
        command = self.last_command
        self.last_command = None
        return command

# Citations
# https://realpython.com/intro-to-python-threading/
# 