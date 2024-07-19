import json
import socket
import threading

# Enum for defining enumerations
from enum import Enum

# WebSocket for real-time communication
from websocket import create_connection, WebSocket


# BhapticsManager class to manage haptic feedback
class BhapticsManager:
    
    # Enum class to define haptic positions
    class BhapticsPosition(Enum):
        Vest = "Vest"
        VestFront = "VestFront"
        VestBack = "VestBack"
        ForearmL = "ForearmL"
        ForearmR = "ForearmR"
        Head = "Head"
        HandL = "HandL"
        HandR = "HandR"
        FootL = "FootL"
        FootR = "FootR"
        GloveL = "GloveL"
        GloveR = "GloveR"
        active_keys = set([])
        connected_positions = set([])

    # Custom WebSocket class to handle incoming frames
    class WebSocketReceiver(WebSocket):
        def recv_frame(self):
            """Receive a frame from the WebSocket server."""
            frame = super().recv_frame()
            try:
                frame_obj = json.loads(frame.data)
                self.active_keys = set(frame_obj['ActiveKeys'])
                self.connected_positions = set(frame_obj['ConnectedPositions'])
            except json.JSONDecodeError:
                print('Failed to decode JSON frame')
            return frame

    def __init__(self):
        """Initialize the BhapticsManager class."""
        self.active_keys = set([])
        self.connected_positions = set([])
        self.ws = None
        self.connected = False
        self.initialize()

    def initialize(self):
        """Initialize the WebSocket connection."""
        try:
            self.ws = create_connection(
                "ws://localhost:15881/v2/feedbacks",
                sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),),
                class_=self.WebSocketReceiver
            )
            threading.Thread(target=self.thread_function).start()
            self.connected = True
        except Exception as e:
            print(f"Couldn't connect: {e}")
            return

    def thread_function(self):
        """Thread function to keep the WebSocket connection alive."""
        while True:
            if self.ws is not None:
                self.ws.recv_frame()

    def destroy(self):
        """Close the WebSocket connection."""
        if self.ws is not None:
            self.ws.close()

    def is_playing(self):
        """Check if any feedback is currently playing."""
        return len(self.active_keys) > 0

    def is_playing_key(self, key):
        """Check if the key is currently playing feedback."""
        return key in self.active_keys

    def is_device_connected(self, position):
        """Check if the device at the given position is connected."""
        return position in self.connected_positions

    def register(self, key, file_directory):
        """Register a key with the given file directory."""
        with open(file_directory, 'r') as f:
            data = json.load(f)
        
        project = data["project"]
        layout = project["layout"]
        tracks = project["tracks"]
        request = {
            "Register": [{
                "Key": key,
                "Project": {
                    "Tracks": tracks,
                    "Layout": layout
                }
            }]
        }
        self.__submit(json.dumps(request))

    def submit_registered(self, key):
        """Submit a registered key."""
        request = {
            "Submit": [{
                "Type": "key",
                "Key": key,
            }]
        }
        self.__submit(json.dumps(request))

    def submit_registered_with_option(self, key, alt_key, scale_option, rotation_option):
        """Submit a registered key with options."""
        request = {
            "Submit": [{
                "Type": "key",
                "Key": key,
                "Parameters": {
                    "altKey": alt_key,
                    "rotationOption": rotation_option,
                    "scaleOption": scale_option,
                }
            }]
        }
        self.__submit(json.dumps(request))

    def submit(self, key, frame):
        """Submit a key with a frame."""
        request = {
            "Submit": [{
                "Type": "frame",
                "Key": key,
                "Frame": frame
            }]
        }
        self.__submit(json.dumps(request))

    def __submit(self, json_str):
        """Send the JSON string to the WebSocket server."""
        if self.ws is not None:
            self.ws.send(json_str)