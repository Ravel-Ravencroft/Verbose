from speech_recognition import Microphone, Recognizer
from blockchain import Blockchain

class VoiceRecogniser:
    ids = ["w1761053", "w1761077", "w1790815"] #TODO: Integrate Teacher ID Module ASAP
    blockchain_object = Blockchain()

    blockchain_object.start_functionality()

    recognizer = Recognizer()

    with Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\nPlease Vocalise Your Student ID: ")
        # audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            edited = text.replace(" ", "").lower()
            print(edited)

            if edited in ids:
                blockchain_object.add_block(edited)
                print("\nThe ID is Valid")
                print( blockchain_object.chain[-1].to_string() )

            else:
                print("The ID is Invalid")
            
            blockchain_object.end_functionality()

        except:
            print("Error: The Speech Could Not Be Recognised")