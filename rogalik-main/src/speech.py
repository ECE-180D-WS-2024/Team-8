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
        self.reset = " "
        self.message = "Press E and say: "
    

    def _listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                print("Say Command")
                self.message = "Say Command"
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1.5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
     
                if self.process_command(command):
                    #print("speech command recognized")
                    if self.callback:
                        self.callback(command)
                else:
      
                    print("Recognition Failed. Press key to try again.")
                    self.message = "Press E to Try Again"
            except sr.RequestError as e:
                # Handle request error, log, or retry logic
        
                print(f"API unavailable, {e}")
                self.message = "Press E to Try Again"
            except sr.UnknownValueError as e:
                # Handle unknown value error, log, or retry logic

                print(f"Could not understand audio {e}")
                self.message = "Press E to Try Again"
            except Exception as e:
       
                print(f"An unexpected error occurred: {e}")
                self.message = "Press E to Try Again"
        self.listening = False
        self.stop_event.set()
        if self.listening == False:
            print("Thread Stopped")
    #     time.sleep(1)

    def toggle_listening(self):
        """Toggle the listening state and manage the listening thread accordingly."""
        if not self.listening:
  
            print("Please wait for speech recognition...")
            self.listening = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._listen)
            self.thread.start()
        else:
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