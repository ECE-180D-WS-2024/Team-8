import speech_recognition as sr

class Speech:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        print("Speech recognizer initialized.")

    def recognize_speech(self):
        """Recognize speech from the microphone and respond to 'pick up' and 'drop' commands."""
        print("Preparing to listen from the microphone...")
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            attempts += 1
            print(f"Attempt {attempts} of {max_attempts}. Say 'pick up' or 'drop'...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=3)
                    transcription = self.recognizer.recognize_google(audio).lower()  # Convert to lowercase to ensure consistency
                    print(f"Recognized: {transcription}")
                    if transcription == "pick up":
                        print("Pick up command recognized.")
                        return "pick up"
                    elif transcription == "drop":
                        print("Drop command recognized.")
                        return "drop"
                    else:
                        print("Command not recognized. Please try again.")
                except sr.RequestError:
                    print("API Error. The speech recognition service is unavailable. Please try again later.")
                    break
                except sr.UnknownValueError:
                    print("Could not understand audio. Please try again.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    break
        print("Failed to recognize command after 3 attempts.")
        return None

if __name__ == "__main__":
    speech = Speech()
    result = speech.recognize_speech()
    if result:
        print(f"Final result: {result}")
    else:
        print("No command recognized.")