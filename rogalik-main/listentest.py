import speech_recognition as sr

r = sr.Recognizer()

speech = sr.Microphone(2)

#print(sr.Microphone.list_microphone_names())

while 1:

             with speech as source:
                 print("say something!…")
                 audio = r.adjust_for_ambient_noise(source)
                 audio = r.listen(source,None,3)
                 print("the audio has been recorded")
             # Speech recognition using Google Speech Recognition
             try:
                 print("api is enabled")
                 recog = r.recognize_google(audio, language = 'en-US')
                 # for testing purposes, we're just using the default API key
                 # to use another API key, use r.recognize_google(audio)
                 # instead of r.recognize_google(audio)

                 print("You said: " + recog)
             except sr.UnknownValueError:
                 print("Google Speech Recognition could not understand audio")
             except sr.RequestError as e:
                 print("Could not request results from Google Speech Recognition service; {0}".format(e))