""" import subprocess



def speak(text):
    subprocess.call(["espeak", "-s140", "Flying state initiated"])


speak("Hello, how are you?")

 """
import pyttsx3

# Initialize the converter
converter = pyttsx3.init()

# Set properties before adding anything to say
# Sets speed percent
# Can be more than 100
converter.setProperty("rate", 150)
# Set volume 0-1
converter.setProperty("volume", 0.7)

# Queue the entered text
# There will be a pause between each one
converter.say("Hello World")
converter.say("I am a text-to-speech program")

# Empties the say() queue
# Program will not continue until all speech is done talking
converter.runAndWait()
