from datetime import date
from os import path, remove
from tkinter import *

from scipy.io.wavfile import write
from sounddevice import rec, wait
from speech_recognition import Microphone, Recognizer

from blockchain import Blockchain
from data_science import check_voice
from server import get_ids, start_blockchain_functionality

GUI = Tk()
GUI.title("Voice Recorder")
GUI.geometry("800x500")
GUI.configure(background='#383b42')

ids = get_ids(True)
fs = 44100
seconds = 10
start_blockchain_functionality()


variable1 = StringVar()
firstLabel = Label(GUI, textvariable=variable1, relief=RAISED)
firstLabel.pack(pady=30)
variable1.set("Please click the button and vocalize your student ID, wait for 3 seconds and start speaking until attendance is marked")


def record_function():
    recordingButton.config(text="Recording audio.....")
    with Microphone() as source:
        Recognizer().adjust_for_ambient_noise(source, duration=1)
        print("\nPlease Vocalise Your Student ID: ")
        audio = Recognizer().listen(source)

        try:
            text = Recognizer().recognize_google(audio)
            text = text.replace(" ", "").lower()
            print(text + "\n")

        except():
            print("Error: The ID Could Not Be Recognised! Please Try Again!")

    if text in ids:
        print("Check-In Phrase: ")
        variable1.set("Please keep speaking to mark your attendance")
        record_phrase = rec(int(seconds * fs), samplerate=fs, channels=1)
        wait()

        print("\nThe ID is Valid")
        file_name = path.abspath("Dataset/Test") + "/" + text + "-" + str(date.today()) + "-8.wav"
        write(file_name, fs, record_phrase)

        if check_voice():
            Blockchain().add_block(id=text, hash=Blockchain().chain[-1].compute_hash())
            variable1.set("Attendance has been marked, thank you")
        else:
            print("Error: The Voice Could Not Be Recognised! Please Try Again!")
            variable1.set("Attendance has not been marked, please try again ")

        remove(file_name)
    else:
        print("The ID is Invalid!")
        variable1.set("The ID could not be recognized, press the button again to record ")


recordButton = PhotoImage(file=r"Images/icon-speech.png")

recordingButton = Button(GUI, image=recordButton, command=record_function, borderwidth=0)
recordingButton.pack(pady=25)

mainloop()