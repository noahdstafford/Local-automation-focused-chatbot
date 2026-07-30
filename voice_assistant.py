import os
# Tool that connects Python to your physical microphone and speakers
import sounddevice as sd
# A digital waiting line where we temporarily store audio data as it comes into the mic
import queue
# This is used to glue tiny chunks of audio data together into one big file
import numpy as np
# Allows Python to listen for physical keystrokes
import keyboard
# Lets us pause the code (sleep) or measure how much time has passed
import time
# A specific tool from the SciPy library that knows how to create a .wav file on the hard drive
from scipy.io.wavfile import write
# Imports open AI's speech to text model
import whisper
from chat import ask_ollama, ask_ollama_chat
# The text-to-speech engine that gives your AI its voice
from piper import PiperVoice
import re
from openwakeword.model import Model

# Load once, outside the main loop
oww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

def listen_for_wake_word(samplerate=16000, chunk_size=1280, threshold=0.5):
    q = queue.Queue()

    def callback(indata, frames, time_info, status):
        q.put(indata.copy())

    with sd.InputStream(channels=1, samplerate=samplerate, blocksize=chunk_size,
                         dtype='int16', callback=callback):
        while True:
            chunk = q.get()
            audio = chunk.flatten()
            prediction = oww_model.predict(audio)

            for mdl_name, score in prediction.items():
                if score > threshold:
                    return

# Defined the clear_screen function so Python knows what it is
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to remove the ai constantly pronouncing asterisks for bolding text
def clean_text_for_speech(text):
    text = re.sub(r'\*+', '', text)   # remove asterisks
    text = re.sub(r'#+', '', text)    # remove hashes
    return text

# Main program
def run_voice_assistant():
    # Loads the whisper model into the coputers memory so its ready
    model = whisper.load_model("small")
    # Loads the specific Northern English Piper voice model into memory
    voice = PiperVoice.load("en_GB-northern_english_male-medium.onnx")

    # AIs memory bank
    conversation_history = []

    # Infinite looping conversation
    while True:

        # Runs function to wait for activation
        listen_for_wake_word()

        # Speak an acknowledgment so the user knows its listening
        greeting = "Yes sir, how can I assist you?"
        greeting_chunks = []
        for chunk in voice.synthesize(greeting):
            greeting_chunks.append(chunk.audio_float_array)
        greeting_audio = np.concatenate(greeting_chunks, axis=0)
        sd.play(greeting_audio, voice.config.sample_rate)
        sd.wait()

        # Creates a fresh, empty waiting line for the audio every time the loop restarts
        q = queue.Queue()

        # Every fraction of a second, this takes the live audio coming into the mic (indata) and safely copies it into the queue
        def my_callback(indata, frames, time, status):
            q.put(indata.copy())

        # Opens the microphone. channels=1 means mono audio
        with sd.InputStream(channels=1, samplerate=44100, callback=my_callback):
            # Pauses the main script, holding the microphone open until you hit the Enter key
            input("Recording... Press Enter to stop.")

        # Creates empty list
        recorded_chunks = []
        # Empties the queue one chunk at a time, dropping them into the list
        while not q.empty():
            recorded_chunks.append(q.get())

        audio_data = np.concatenate(recorded_chunks, axis=0)
        # Saves that glued-together track to your hard drive as my_recording.wav
        write("my_recording.wav", 44100, audio_data)

        result = model.transcribe("my_recording.wav", language="en")
        transcribed_text = result["text"]


        print("You said:", transcribed_text)

        # Add your words to the memory bank
        conversation_history.append({"role": "user", "content": transcribed_text})

        # Send the memory bank to the chat function
        answer = ask_ollama_chat(conversation_history)
        clean_answer = clean_text_for_speech(answer)

        # Add the AIs answer to the memory bank so it remembers what it said!
        conversation_history.append({"role": "assistant", "content": clean_answer})

        # Creates a new empty list to hold the AI's synthesized voice data
        audio_chunks = []
        # Feeds the clean text to Piper
        for chunk in voice.synthesize(clean_answer):
            audio_chunks.append(chunk.audio_float_array)

        # Glues Piper's audio chunks together into one playable track
        response_audio = np.concatenate(audio_chunks, axis=0)

        # Sends the synthesized audio track the laptops physical speakers
        sd.play(response_audio, voice.config.sample_rate)
        # Creates a loop that runs continuously while the AI is speaking.
        while sd.get_stream().active:
            # If you tap the 'Q' key during the speech, it triggers the next lines
            if keyboard.is_pressed('q'):
                # Instantly kills the audio stream and breaks the loop
                sd.stop()
                print("Stopped talking.")
                break
            # A tiny pause so the loop doesn't run a million times a second and crash the computers processor
            time.sleep(0.1)

        # If q isnt pressed it wiats until audio file finished
        sd.wait()

        print("Press Q to quit, or wait to ask another question...")
        # Records the exact time on the clock at taht moment 
        start_time = time.time()
        # Creates a loop that runs until exactly 5 seconds have passed
        while time.time() - start_time < 5:
            # If q pressed in 5 second windo it says goodebye and uses return to exit the run voice assistant function shuttting down the program
            if keyboard.is_pressed('q'):
                print("Goodbye!")
                return
            time.sleep(0.1)

        clear_screen()

if __name__ == "__main__":
    run_voice_assistant()