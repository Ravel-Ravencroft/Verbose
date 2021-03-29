import speech_recognition as sr
from blockchain import Blockchain

class main:
    ids = ["w1761053", "w1761077", "w1790815"] #Remove in Future Iteration
    blockchain_object = Blockchain()
    blockchain_object.start_functionality()

    r = sr.Recognizer()
    print(sr.Microphone.list_microphone_names())

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("say anything : ")
        # audio = r.listen(source, timeout=1, phrase_time_limit=10)
        audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            edited = text.replace(" ", "").lower()
            print(edited)

            if edited in ids:
                blockchain_object.add_block(edited)
                blockchain_object.print_blockchain()
                print("The ID is Valid")
            else:
                print("The ID is Invalid")
            
            blockchain_object.end_functionality()
        except:
            print("Sorry could not recognize the words you said")