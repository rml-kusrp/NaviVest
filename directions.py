import vest
import os
from gtts import gTTS

class Directions:

    def __init__(self):
        self.bhaptics_manager = vest.BhapticsManager()
        self.bhaptics_manager.register("forward", "assets/tacts/FF.tact ")
        self.bhaptics_manager.submit_registered("forward")
        self.bhaptics_manager.register("backward", "assets/tacts/BB.tact")
        self.bhaptics_manager.submit_registered("backward")
        self.bhaptics_manager.register("right", "assets/tacts/RR.tact")
        self.bhaptics_manager.submit_registered("right")
        self.bhaptics_manager.register("left", "assets/tacts/LL.tact")
        self.bhaptics_manager.submit_registered("left")

    def fwd(self, intensity):
        # self.bhaptics_manager.submit_registered_with_option(key="forward", scale_option=intensity)  eski
        self.bhaptics_manager.submit_registered_with_option(
            "forward", "alt2",
            scale_option={"intensity": intensity, "duration": 1},
            rotation_option={"offsetAngleX": 0, "offsetY": 0}
        )
        print("pressed forward")

    def bwd(self, intensity):
        self.bhaptics_manager.submit_registered_with_option(
            "backward", "alt2",
            scale_option={"intensity": intensity, "duration": 1},
            rotation_option={"offsetAngleX": 0, "offsetY": 0}
        )
        print("pressed backward")

    def right(self, intensity):
        self.bhaptics_manager.submit_registered_with_option(
            "right", "alt2",
            scale_option={"intensity": intensity, "duration": 1},
            rotation_option={"offsetAngleX": 0, "offsetY": 0}
        )
        print("pressed right")

    def left(self, intensity):
        self.bhaptics_manager.submit_registered_with_option(
            "left", "alt2",
            scale_option={"intensity": intensity, "duration": 1},
            rotation_option={"offsetAngleX": 0, "offsetY": 0}
        )
        print("pressed left")

    # def play_voice(self, mytext):
    #     language = 'tr'
    #     myobj = gTTS(text=mytext, lang=language, slow=False)
    #     print("Saving is started")
    #     myobj.save("messageOfComputer.wav")
    #     print("Saved and will play")
    #     os.system("start messageOfComputer.wav") #windows'da afplay yerine start yazman gerek
    #     print("Played")