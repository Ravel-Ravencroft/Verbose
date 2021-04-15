import speech_recognition as sr

r=sr.Recognizer()
print(sr.Microphone.list_microphone_names())
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)
    print("say anything : ")
    # audio = r.listen(source, timeout=1, phrase_time_limit=10)
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(text)
    except:
        print("Sorry could not recognize the words you said")