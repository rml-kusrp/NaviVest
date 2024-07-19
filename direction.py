import os
from gtts import gTTS
import time
import keyboard
from directions import Directions
directions = Directions()
intensity = 100  # Example intensity value (adjust as needed)

class PathNavigator:
    def __init__(self, graph, orientation="up"):
        self.orientation = orientation

        self.graph = graph

        

     



        
        # self.index_map = self.create_index_map()
        self.directions = ""

    # def create_index_map(self):
    #     return {self.grid[row][col]: (row, col) for row in range(len(self.grid)) for col in range(len(self.grid[row])) if self.grid[row][col] in range(6)}

    # def read_user_path(self):
    #     with open(self.user_path_file, 'r') as f:
    #         return f.read().strip()

    def parse_pairs(self, the_road_taken):
        return the_road_taken

    def determine_directions(self, pairs):
        for i in range(len(pairs) - 1):
            first, second = pairs[i], pairs[i + 1]

            
            row1, col1 = first
            row2, col2 = second

            print(row1 , row2, col1, col2)

            if col2 < col1:
                self._add_direction("left", "turn backwards and go forward", "go forward", "turn left and go forward", "turn right and go forward")
                self.orientation = "left"
                
            elif col2 > col1:
                self._add_direction("right", "go forward", "turn backwards and go forward", "turn right and go forward", "turn left and go forward")
                self.orientation = "right"
            if row2 > row1:
                self._add_direction("down", "turn right and go forward", "turn left and go forward", "turn backwards and go forward", "go forward")
                self.orientation = "down"
            elif row2 < row1:
                self._add_direction("up", "turn left and go forward", "turn right and go forward", "go forward", "go backwards and go forward")
                self.orientation = "up"

    def _add_direction(self, new_orientation, right_cmd, left_cmd, up_cmd, down_cmd):
        if self.orientation == "left":
            # self.directions += left_cmd + "; "
            self.play_voice(left_cmd)
            if (left_cmd=="turn backwards and go forward"):
                directions.bwd(intensity)
            if (left_cmd=="turn right and go forward"):
                directions.right(intensity)
            if (left_cmd=="turn left and go forward"):
                directions.left(intensity)
            if (left_cmd=="go forward"):
                directions.fwd(intensity)
            print("working")
            time.sleep(3)
        elif self.orientation == "right":
            # self.directions += right_cmd + "; "
            self.play_voice(right_cmd)
            if (right_cmd=="turn backwards and go forward"):
                directions.bwd(intensity)
            if (right_cmd=="turn right and go forward"):
                directions.right(intensity)
            if (right_cmd=="turn left and go forward"):
                directions.left(intensity)
            if (right_cmd=="go forward"):
                directions.fwd(intensity)
            print("working")
            time.sleep(3)
        elif self.orientation == "up":
            # self.directions += up_cmd + "; "
            self.play_voice(up_cmd)
            if (up_cmd=="turn backwards and go forward"):
                directions.bwd(intensity)
            if (up_cmd=="turn right and go forward"):
                directions.right(intensity)
            if (up_cmd=="turn left and go forward"):
                directions.left(intensity)
            if (up_cmd=="go forward"):
                directions.fwd(intensity)
            print("working")
            time.sleep(3)
        elif self.orientation == "down":
            # self.directions += down_cmd + "; "
            self.play_voice(down_cmd)
            if (down_cmd=="turn backwards and go forward"):
                directions.bwd(intensity)
            if (down_cmd=="turn right and go forward"):
                directions.right(intensity)
            if (down_cmd=="turn left and go forward"):
                directions.left(intensity)
            if (down_cmd=="go forward"):
                directions.fwd(intensity)
            print("working")
            time.sleep(3)

        print(self.directions)

    # def write_directions(self):
    #     with open(self.directions_file, 'w') as f:
    #         f.write(self.directions.strip())

    def execute_script(self, script_path):
        os.system(f"python3 {script_path}")

    def play_voice(self, mytext):
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("messageOfComputer.mp3")
        os.system("start messageOfComputer.mp3")

    def run(self):
        print("run started")

        old = None
        

        graphpath = self.graph.pathID
        print(graphpath)

        while True:
            if self.graph.pathID is not None and self.graph.pathID != old:
                old = self.graph.pathID

                pairs = self.parse_pairs(self.graph.pathID)
                self.determine_directions(pairs)

                print("yes")

            if keyboard.is_pressed('q'):
                print("Exiting...")
                break

      
            
            
             


        # self.path = [(4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4)]
        # self.path = [(8, 4), (8, 3), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2)]
      