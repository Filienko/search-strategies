import datetime
import numpy as np
import re
from Solver import Node, bfs, greedy, a, dfs

# GOAL STATES, given the appropriate size of a game setting to search the state for by a method
GOAL_STATES = {
    2: np.array([['2', '1'],
                 ['3', ' ']]),
    3: np.array([[' ', '1', '2'],
                 ['3', '4', '5'],
                 ['6', '7', '8']]),
    4: np.array([['1', '2', '3', '4'],
                 ['5', '6', '7', '8'],
                 ['9', 'A', 'B', 'C'],
                 ['D', 'E', 'F', ' ']]),
    5: np.array([[' ', '1', '2', '3', '4'],
                 ['5', '6', '7', '8', '9'],
                 ['A', 'B', 'C', 'D', 'E'],
                 ['F', 'G', 'H', 'I', 'J'],
                 ['K', 'L', 'M', 'N', 'O']]),
    6: np.array([[' ', '0', '1', '2', '3', '4'],
                 ['5', '6', '7', '8', '9', 'A'],
                 ['B', 'C', 'D', 'E', 'F', 'G'],
                 ['H', 'I', 'J', 'K', 'L', 'M'],
                 ['N', 'O', 'P', 'Q', 'R', 'S'],
                 ['T', 'U', 'V', 'W', 'X', 'Y']]),
    7: np.array([[' ', '0', '1', '2', '3', '4', '5'],
                 ['6', '7', '8', '9', 'A', 'B', 'C'],
                 ['D', 'E', 'F', 'G', 'H', 'I', 'J'],
                 ['K', 'L', 'M', 'N', 'O', 'P', 'Q'],
                 ['R', 'S', 'T', 'U', 'V', 'W', 'X'],
                 ['Y', 'Z', 'a', 'b', 'c', 'd', 'e'],
                 ['f', 'g', 'h', 'i', 'j', 'k', 'l']]),
}


# Contains certain limited environment mechanics
class Board:
    def __init__(self, size: int, initial_state: Node, search_method: str, history: list,
                 final_state: Node):
        self.size = size
        self.initial_state = initial_state
        self.search_method = search_method
        self.final_state = final_state
        self.history = history

    def __init__(self, string: str):
        pattern = r'"([^"]*)"'
        puzzle_elements = re.findall(pattern, string)
        tokens = string.split(" ")
        self.size = int(tokens[0])
        self.initial_state = puzzle_elements
        self.search_method = tokens[-1]
        self.final_state = []
        self.history = []

    def manhattan_distance(self, node: Node) -> int:
        sums = 0
        arr = node.state
        for y1, x1 in np.ndindex(arr.shape):
            item: str = arr[y1, x1]
            y2, x2 = np.asarray(np.where(self.final_state.state == item)).T[0]
            sums += abs(y1 - y2) + abs(x1 - x2)

        return sums

    # Sets initial and final state of a board to determine the moves
    def initialize_game(self):
        to_array = []

        for x in self.initial_state:
            to_array.extend(x)

        self.initial_state = Node(
            np.array([[to_array[x + y * self.size] for x in range(0, self.size)] for y in range(0, self.size)]), 0, -1,
            -1, 0, (0, 0))
        self.initial_state.blank_coordinate = np.asarray(np.where(self.initial_state.state == ' ')).T[0]
        self.final_state = Node(GOAL_STATES[self.size], 0, -1, -1, 0, (0, 0))
        self.final_state.blank_coordinate = np.asarray(np.where(self.final_state.state == ' ')).T[0]

        if self.search_method == "BFS":
            self.bfs_output()
        elif self.search_method == "DFS":
            self.dfs_output()
        elif self.search_method == "GBFS":
            self.greedy_output()
        elif self.search_method == "AStar":
            self.a_output()

    def bfs_output(self):
        depth, max_num, exp, fringe_len = bfs(self)

        f = open("ReadMe.txt", "a")
        f.write("\n--------------")
        f.write(f"\nSize: {self.size}")
        f.write(f"\ninitial: {self.initial_state}")
        f.write(f"\ngoal: {self.final_state}")
        f.write(f"\nSearch Method: BFS")
        f.write(f"\n{depth}, {max_num}, {exp}, {fringe_len}")
        f.close()

    def dfs_output(self):
        depth, max_num, exp, fringe_len = dfs(self)

        f = open("ReadMe.txt", "a")
        f.write("\n--------------")
        f.write(f"\nSize: {self.size}")
        f.write(f"\ninitial: {self.initial_state}")
        f.write(f"\ngoal: {self.final_state}")
        f.write(f"\nSearch Method: DFS")
        f.write(f"\n{depth}, {max_num}, {exp}, {fringe_len}")
        f.close()

    def a_output(self):
        depth, max_num, exp, fringe_len = a(self)

        f = open("ReadMe.txt", "a")
        f.write("\n--------------")
        f.write(f"\nSize: {self.size}")
        f.write(f"\ninitial: {self.initial_state}")
        f.write(f"\ngoal: {self.final_state}")
        f.write(f"\nSearch Method: AStar")
        f.write(f"\n{depth}, {max_num}, {exp}, {fringe_len}")
        f.close()

    def greedy_output(self):
        depth, max_num, exp, fringe_len = greedy(self)

        f = open("ReadMe.txt", "a")
        f.write("\n--------------")
        f.write(f"\nSize: {self.size}")
        f.write(f"\ninitial: {self.initial_state}")
        f.write(f"\ngoal: {self.final_state}")
        f.write(f"\nSearch Method: Greedy")
        f.write(f"\n{depth}, {max_num}, {exp}, {fringe_len}")
        f.close()


    def __repr__(self) -> str:
        return f"{type(self).__name__}(size={self.size}, search method={self.search_method})\n"
