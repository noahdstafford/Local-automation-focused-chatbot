import sounddevice as sd
import queue
import numpy as np
from scipy.io.wavfile import write
import whisper
from chat import ask_ollama

q = queue.Queue()

def my_callback(indata, frames, time, status):
    q.put(indata.copy())

with sd.InputStream(channels=1, samplerate=44100, callback=my_callback):
    input("Recording... Press Enter to stop.")

recorded_chunks = []
while not q.empty():
    recorded_chunks.append(q.get())

audio_data = np.concatenate(recorded_chunks, axis=0)
write("my_recording.wav", 44100, audio_data)

model = whisper.load_model("small")
result = model.transcribe("my_recording.wav", language="en")
transcribed_text = result["text"]

print("You said:", transcribed_text)

answer = ask_ollama(transcribed_text)

from piper import PiperVoice
import numpy as np
from scipy.io.wavfile import write

voice = PiperVoice.load("en_GB-northern_english_male-medium.onnx")

audio_chunks = []
for chunk in voice.synthesize(answer):
    audio_chunks.append(chunk.audio_float_array)

response_audio = np.concatenate(audio_chunks, axis=0)

sd.play(response_audio, voice.config.sample_rate)
sd.wait()