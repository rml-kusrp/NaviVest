from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMainWindow, QApplication, QTextEdit, QSlider, QHBoxLayout
from PySide6.QtCore import Qt
import directions
import keyboard
from directions import Directions
import sys
#import sounddevice as sd
#import numpy as np
import queue
import threading
import wave
import speech_recognition as sr
from gtts import gTTS
import os
import pyaudio

class VoiceRecorder:
    def __init__(self, ui, direc):
        #direc yeni eklendi
        self.direc = direc #yeni eklendi
        self.ui = ui
        self.is_recording = False
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None

        # No need to create the Start Recording button here

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
            self.ui.log_message("Kayıt bitti")
        else:
            self.start_recording()
            self.ui.log_message("Kayıt başladı")

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=3200
        )
        threading.Thread(target=self.record).start()

    def stop_recording(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        try:
            threading.Thread(target=self.save_recording).start()
        except:
            print("Uyarı")

    def record(self):
        while self.is_recording:
            data = self.stream.read(3200)
            self.frames.append(data)

    def save_recording(self):
        wf = wave.open("user.wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        try:
            self.recognize_and_respond()
        except:
            print("Lütfen tekrar deneyin")

    def recognize_and_respond(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile("user.wav") as source:
            audio = recognizer.record(source)
        recognized_text = recognizer.recognize_google(audio, language="tr-TR")

        print(recognized_text)

        if "ileri" in recognized_text:
            self.ui.send_feedback("Sesli ileti anlaşıldı: ileri")
            self.direc.fwd(self.ui.intensity)
            os.system("start assets/audio/ileri.wav")

        elif "geri" in recognized_text:
            self.ui.send_feedback("Sesli ileti anlaşıldı: geri")
            self.direc.bwd(self.ui.intensity)
            os.system("start assets/audio/geri.wav")

        elif "sol" in recognized_text:
            self.ui.send_feedback("Sesli ileti anlaşıldı: sol")
            self.direc.left(self.ui.intensity)
            os.system("start assets/audio/sol.wav")

        elif "sağ" in recognized_text:
            self.ui.send_feedback("Sesli ileti anlaşıldı: sağ")
            self.direc.right(self.ui.intensity)
            os.system("start assets/audio/sağ.wav")

        else:
            print("Dediğinizi anlamadım")

class UI(QMainWindow):
    def __init__(self, direc):
        super().__init__()

        self.setWindowTitle("Yelek Arayüzü")
        self.setMinimumSize(400, 300)

        self.direc = direc
        self.voice_recorder = VoiceRecorder(self, direc) #yeni eklendi

        # Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Intensity Slider
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(0, 4)
        self.intensity_slider.setValue(1)
        self.intensity = 1
        self.intensity_slider.setTickInterval(0.1)
        self.intensity_slider.setTickPosition(QSlider.TicksBelow)
        self.intensity_slider.valueChanged.connect(self.slider_value_changed)
        layout.addWidget(self.intensity_slider)

        # Arrow Buttons
        arrow_layout = QHBoxLayout()
        layout.addLayout(arrow_layout)

        arrow_up_button = QPushButton("↑")
        arrow_up_button.pressed.connect(lambda: self.send_feedback("Yazılı ileti anlaşıldı: ileri"))
        arrow_up_button.pressed.connect(lambda: self.direc.fwd(self.intensity))
        arrow_up_button.pressed.connect(lambda: os.system("start assets/audio/ileri.wav"))
        arrow_layout.addWidget(arrow_up_button)

        arrow_down_button = QPushButton("↓")
        arrow_down_button.pressed.connect(lambda: self.send_feedback("Yazılı ileti anlaşıldı: geri"))
        arrow_down_button.pressed.connect(lambda: self.direc.bwd(self.intensity))
        arrow_down_button.pressed.connect(lambda: os.system("start assets/audio/geri.wav"))
        arrow_layout.addWidget(arrow_down_button)

        arrow_left_button = QPushButton("←")
        arrow_left_button.pressed.connect(lambda: self.send_feedback("Yazılı ileti anlaşıldı: sol"))
        arrow_left_button.pressed.connect(lambda: self.direc.left(self.intensity))
        arrow_left_button.pressed.connect(lambda: os.system("start assets/audio/sol.wav"))
        arrow_layout.addWidget(arrow_left_button)

        arrow_right_button = QPushButton("→")
        arrow_right_button.pressed.connect(lambda: self.send_feedback("Yazılı ileti anlaşıldı: sağ"))
        arrow_right_button.pressed.connect(lambda: self.direc.right(self.intensity))
        arrow_right_button.pressed.connect(lambda: os.system("start assets/audio/sağ.wav"))
        arrow_layout.addWidget(arrow_right_button)

        # Voice Command Button (Replaces Start Recording button)
        self.voice_command_button = QPushButton("Sesli Komut")
        self.voice_command_button.clicked.connect(self.toggle_voice_command)
        layout.addWidget(self.voice_command_button)

        # Log Panel
        self.log_textedit = QTextEdit()
        layout.addWidget(self.log_textedit)

    def slider_value_changed(self, value):
        self.send_feedback(f"Şiddetin güncellendiği değer: {value}")
        self.intensity = value

    def send_feedback(self, message):
        self.log_message(message)

    def log_message(self, message):
        self.log_textedit.append(message)

    def toggle_voice_command(self):
        self.voice_recorder.toggle_recording()

if __name__ == "__main__":
    direc = Directions()
    app = QApplication(sys.argv)
    main_window = UI(direc)
    main_window.show()
    sys.exit(app.exec())
