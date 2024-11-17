import pyttsx3
import keyboard

# Create a text-to-speech engine
engine = pyttsx3.init()

# Prompt the user for input
text = input("Enter some text: ")

# Split the text into sentences
sentences = text.split("。")

# Loop through each sentence
for sentence in sentences:
    # Speak the sentence when user presses a key
    print("Press any key to read the next sentence")
    keyboard.wait(" ")
    engine.say(sentence)
    engine.runAndWait()
