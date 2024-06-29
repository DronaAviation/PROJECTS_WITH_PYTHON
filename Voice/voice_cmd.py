from vosk import Model, KaldiRecognizer
import pyaudio
import json
from plutocontrol import pluto

# Initialize Vosk model for speech recognition
model = Model(r"/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

# Initialize PyAudio for microphone input
mic = pyaudio.PyAudio()  # Make sure your microphone is enabled and working
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)  # Increased buffer size
stream.start_stream()

# Initialize Pluto object for controlling the drone
my_pluto = pluto()

# Continuously listen for speech input and recognize it
while True:
    data = stream.read(4096)
    
    # Process the received audio data for speech recognition
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        data = json.loads(text)
        recognized_text = data["text"]
        print("Recognized:", recognized_text)
        
        # Execute drone commands based on recognized speech
        if "start" in recognized_text:
            my_pluto.arm()
        elif "fly" in recognized_text:
            my_pluto.take_off()
        elif "stop" in recognized_text:
            my_pluto.disarm()
        elif "land" in recognized_text:
            my_pluto.land()
        elif "up" in recognized_text:
            my_pluto.increase_height()
        elif "down" in recognized_text:
            my_pluto.decrease_height()
        elif "forward" in recognized_text:
            my_pluto.forward()
        elif "back" in recognized_text:
            my_pluto.backward()
        elif "left" in recognized_text:
             my_pluto.left()
        elif "right" in recognized_text:
            my_pluto.right()
        elif "yes" in recognized_text:
            my_pluto.left_yaw()
        elif "no" in recognized_text:
            my_pluto.right_yaw()
        
        # Add more commands as needed
        
    else:
        print("No speech detected or recognized.")
