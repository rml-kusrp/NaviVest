from path import DynamicGraph
from aruco_read import ArucoMarkerDetector
import threading
from direction import PathNavigator

def graph_function(graph):
    graph.run()

def aruco_function(aruco):
    aruco.run()

def direction_function(direction):
    direction.run()



if __name__ == "__main__":
    aruco = ArucoMarkerDetector()
    graph = DynamicGraph(aruco)
    direction= PathNavigator(graph=graph)


    print("Aruco and graph are initialized.")

    graph_thread = threading.Thread(target=graph_function, args=(graph,))
    aruco_thread = threading.Thread(target=aruco_function, args=(aruco,))
    direction_thread = threading.Thread(target=direction_function, args=(direction,))

    graph_thread.start()
    aruco_thread.start()
    direction_thread.start()

    print("Threads are started")

    graph_thread.join()
    aruco_thread.join()
    direction_thread.join()