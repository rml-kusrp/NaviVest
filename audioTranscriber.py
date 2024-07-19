import tkinter as tk
import pyaudio
import wave
import speech_recognition as sr
from gtts import gTTS
import os

class VoiceRecorder:
    def __init__(self, master):
        self.master = master
        self.is_recording = False
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None

        self.button = tk.Button(master, text="Start Recording", command=self.toggle_recording)
        self.button.pack(pady=20)

        self.master.bind('<space>', self.toggle_recording_event)

    def toggle_recording_event(self, event):
        self.toggle_recording()

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.button.config(text="Stop Recording")
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=3200
        )
        self.record()

    def stop_recording(self):
        self.is_recording = False
        self.button.config(text="Start Recording")
        self.stream.stop_stream()
        self.stream.close()
        self.save_recording()
        self.recognize_and_respond()

    def record(self):
        if self.is_recording:
            data = self.stream.read(3200)
            self.frames.append(data)
            self.master.after(1, self.record)

    def save_recording(self):
        wf = wave.open("messageOfUser.wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(self.frames))
        wf.close()
    
    def play_voice(self, mytext):
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("messageOfComputer.mp3")
        os.system("afplay messageOfComputer.mp3") #windows'da afplay yerine start yazman gerek


    def recognize_and_respond(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile("messageOfUser.wav") as source:
            audio = recognizer.record(source)
        recognized_text = recognizer.recognize_google(audio)
        if "left" in recognized_text and "right" not in recognized_text:
            mytext = "Looking at the left"
            self.play_voice(mytext)
        elif "right" in recognized_text and "left" not in recognized_text:
            mytext = "Looking at the right"
            self.play_voice(mytext)
        else:
            mytext = ("Invalid comment, either the word left or the word right must be mentioned in the voice recording")
            self.play_voice(mytext)


# Create a Tkinter window
window = tk.Tk()
window.title("Voice Recorder")

# Create a VoiceRecorder instance
recorder = VoiceRecorder(window)

# Run the Tkinter main loop
window.mainloop()
