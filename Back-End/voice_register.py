from datetime import date
from os import path
from scipy.io.wavfile import write
from sounddevice import rec, wait
from speech_recognition import Microphone, Recognizer


fs = 44100
seconds = 10
r = Recognizer()
today = date.today()

with Microphone() as source:
    r.adjust_for_ambient_noise(source, duration = 1)
    print("\nPlease Vocalise Your Student ID: ")
    audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        text = text.replace(" ", "").lower()
        print(text + "\n")

    except:
        print("Error: The ID Could Not Be Recognised! Please Try Again!")

print("Phrase 1: Hi This is phrase 1  ")
recordPhrase1 = rec(int(seconds * fs), samplerate=fs, channels=1)
wait()

print("Phrase 2: Hi This is phrase 2  ")
recordPhrase2 = rec(int(seconds * fs), samplerate=fs, channels=1)
wait()

print("Phrase 3: Hi This is phrase 3  ")
recordPhrase3 = rec(int(seconds * fs), samplerate=fs, channels=1)
wait()

print("Phrase 4: Hi This is phrase 4  ")
recordPhrase4 = rec(int(seconds * fs), samplerate=fs, channels=1)
wait()

print("Phrase 5: Hi This is phrase 5  ")
recordPhrase5 = rec(int(seconds * fs), samplerate=fs, channels=1)
wait()

print("Phrase 6: Hi This is phrase 6  ")
recordPhrase6 = rec(int(seconds * fs), samplerate=fs, channels=1)
wait()

print("Phrase 7: Hi This is phrase 7  ")
recordPhrase7 = rec(int(seconds * fs), samplerate=fs, channels=1)
wait()

directory_path = path.abspath("Dataset")

write(directory_path + "/Train/" + text + "-" + str(today) + "-1.flac", fs, recordPhrase1)
write(directory_path + "/Train/" + text + "-" + str(today) + "-2.flac", fs, recordPhrase2)
write(directory_path + "/Train/" + text + "-" + str(today) + "-3.flac", fs, recordPhrase3)
write(directory_path + "/Train/" + text + "-" + str(today) + "-4.flac", fs, recordPhrase4)
write(directory_path + "/Validate/" + text + "-" + str(today) + "-5.flac", fs, recordPhrase5)
write(directory_path + "/Validate/" + text + "-" + str(today) + "-6.flac", fs, recordPhrase6)
write(directory_path + "/Validate/" + text + "-" + str(today) + "-7.flac", fs, recordPhrase7)