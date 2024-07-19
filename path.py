from aruco_read import ArucoMarkerDetector  
import networkx as nx
import heapq
import keyboard



# class Person:
#     def __init__(self, direction, nodes, path):



class DynamicGraph:
    def __init__(self, aruco, start=(6, 2), goal=(2, 2)):
        self.G = nx.Graph()
        self.pathID = None
        self.start = start
        self.goal = goal
        self.aruco = aruco
        self.nodes = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10),
            (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
        ]
        
        self.squares = [
            (0, 1), (0, 2), (1, 1), (1, 2), 
            (0, 4), (0, 5), (1, 4), (1, 5), 
            (0, 9), (0, 10), (1, 9), (1, 10), 
            (3, 0), (3, 1), (4, 0), (4, 1), 
            (3, 3), (3, 4), (4, 3), (4, 4),
            (3, 6), (3, 7), (4, 6), (4, 7),
            (4, 9), (4, 10), (5, 9), (5, 10),
            (6, 0), (6, 1), (7, 0), (7, 1),
            (6, 3), (6, 4), (7, 3), (7, 4),
            (6, 6), (6, 7), (7, 6), (7, 7),      
        ]
        
        self.add_nodes()
        self.add_edges()
        self.graph_array = self.create_graph_array()
        
        self.marker_positions = {
            6: (7, 9), 7: (8, 7), 8: (8, 4), 9: (8, 0), 10: (5, 8), 11: (5, 7), 12: (5, 5), 13: (5, 2), 14: (3, 10), 15: (2, 8), 16: (2, 5), 17: (2, 2), 18: (2, 0), 19: (0, 8), 24: (0, 3), 25: (0, 0)
        }

    def add_nodes(self):
        self.G.add_nodes_from(self.nodes)
        
    def add_edges(self):
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                node1 = self.nodes[i]
                node2 = self.nodes[j]
                if (node1 not in self.squares and node2 not in self.squares and
                    ((abs(node1[0] - node2[0]) == 1 and node1[1] == node2[1]) or
                     (abs(node1[1] - node2[1]) == 1 and node1[0] == node2[0]))):
                    self.G.add_edge(node1, node2)

    def create_graph_array(self):
        max_x = max(node[0] for node in self.nodes) + 1
        max_y = max(node[1] for node in self.nodes) + 1
        graph_array = [[' ' for _ in range(max_y)] for _ in range(max_x)]
        
        for node in self.nodes:
            graph_array[node[0]][node[1]] = '.'
        
        for node in self.squares:
            graph_array[node[0]][node[1]] = '#'
        
        graph_array[self.start[0]][self.start[1]] = 'S'
        graph_array[self.goal[0]][self.goal[1]] = 'G'
        
        return graph_array
    
    def print_graph(self):
        for row in self.graph_array:
            print(' '.join(row))

    def update_start(self, marker_id):
        new_start = self.marker_positions.get(marker_id)
        if new_start:
            self.start = new_start
            path = self.astar_path(self.start, self.goal)
            self.update_graph_array(path)
            self.print_graph()
        else:
            print("Marker ID not recognized.")

    def heuristic(self, node, goal):
        return abs(goal[0] - node[0]) + abs(goal[1] - node[1])

    def astar_path(self, start, goal):
        queue = [(0, start)]
        heapq.heapify(queue)
        came_from = {}
        cost_so_far = {start: 0}
        
        while queue:
            current_cost, current_node = heapq.heappop(queue)
            
            if current_node == goal:
                break
            
            for next_node in self.G.neighbors(current_node):
                new_cost = cost_so_far[current_node] + 1  
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(next_node, goal)
                    heapq.heappush(queue, (priority, next_node))
                    came_from[next_node] = current_node
        
        if goal not in came_from:
            print("No path found from", start, "to", goal)
            return None
        
        path = []
        node = goal
        while node != start:
            path.append(node)
            node = came_from[node]
        path.append(start)
        path.reverse()
        
        self.pathID = path


        return path

    def update_graph_array(self, path):
        for i in range(len(self.graph_array)):
            for j in range(len(self.graph_array[0])):
                if (i, j) in self.squares:
                    self.graph_array[i][j] = '#'
                elif (i, j) == self.start:
                    self.graph_array[i][j] = 'S'
                elif (i, j) == self.goal:
                    self.graph_array[i][j] = 'G'
                elif (i, j) in path:
                    self.graph_array[i][j] = '*'
                else:
                    self.graph_array[i][j] = '.'

    def run(self):
        old = None

        while True:
            if self.aruco.arucoID is not None and self.aruco.arucoID != old and self.aruco.arucoID != 0 and self.aruco.arucoID != 1023:
                old = self.aruco.arucoID
                print(self.aruco.arucoID)
                self.update_start(self.aruco.arucoID)

            if keyboard.is_pressed('q'):
                print("Exiting...")
                break