import speech_recognition as sr
from datetime import datetime
import pyttsx3

def greet():
    return "Hello! How can I help you today?"

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}"

def main():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    print("Initializing voice assistant...")

    while True:
        with sr.Microphone() as source:
            print("Say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You said:", user_input)

            if "hello" in user_input:
                response = greet()
            elif "time" in user_input:
                response = get_time()
            elif "exit" in user_input:
                print("Exiting voice assistant...")
                break
            else:
                response = "I'm sorry, I didn't understand that."

            print("Assistant:", response)
            engine.say(response)
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

main()