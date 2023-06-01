import numpy as np

# LIMIT for DFS, as a result of a local machine time limitation and space size
# allowed that, so that it does not run excessive amount of time if no solution can be found by DPS
# Added that set of numbers due to the available time/hardware set
# constraints, implemented that to produce output faster.
DEPTH_LIMITS = {
    2: 16,
    3: 64,
    4: 128,
    5: 256,
    6: 1024,
    7: 1024,
}


# Allows a Node to print current path of a node to a farthest parent (a puzzle initial state)
def display_path(node, board):
    while node != board.initial_state:
        print(node.state)
        node = node.parent

    return node.depth


# Node class, containing the 2d array of a current state of an environment of a current puzzle
class Node:
    def __init__(self, state: np.ndarray, parent: object, heuristic: int, actual_cost: int, depth: int,
                 blank_coordinate: tuple):
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.depth = depth
        self.blank_coordinate = blank_coordinate

    def __repr__(self) -> str:
        return_string = "\n"
        for row in self.state:
            return_string = return_string + str(row) + "\n"
        return return_string

    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        """Overrides the default implementation"""
        return (self.state == other.state).all()

    def __cmp__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        if self.depth == -1:
            return self.heuristic - other.heuristic
        """Overrides the default implementation"""
        return (self.depth + self.heuristic) - (other.depth + other.heuristic)

    def __hash__(self):
        return hash(str(self.state))


# All of the classes produce children at depth -1, all variation may be due to an order of expansion
# of the current children group
def branch(node: Node, board):
    child_nodes = []

    blank_coordinate = node.blank_coordinate
    moving_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for direction in moving_directions:
        new_y, new_x = blank_coordinate[0] + direction[0], blank_coordinate[1] + direction[1]

        if board.size > new_x >= 0 and board.size > new_y >= 0:
            child_node = Node(np.copy(node.state), node, -1, -1, node.depth + 1, (0, 0))
            temp = node.state[new_y, new_x]
            child_node.state[new_y, new_x] = ' '
            child_node.state[blank_coordinate[0], blank_coordinate[1]] = temp
            child_node.blank_coordinate = (new_y, new_x)
            child_nodes.append(child_node)
            child_node.heuristic = board.manhattan_distance(child_node)
    return child_nodes


def bfs(board):
    fringe: list = [board.initial_state]
    expanded: set = {board.initial_state}

    max_num = 0
    exp = 0
    fringe_lens = {0}
    fringe_len = 1
    depth = -1

    # Visits and expands the first available child-node
    while len(fringe) > 0:
        node = fringe[0]
        fringe.remove(node)
        fringe_len = fringe_len - 1
        expanded.add(node)
        exp += 1
        if board.final_state != node:
            child_nodes = branch(node, board)
            child_nodes_len = len(child_nodes)
            max_num = max_num + child_nodes_len
            fringe_len = fringe_len + child_nodes_len
            for child_node in child_nodes:
                if child_node not in expanded:
                    fringe.append(child_node)
            fringe_lens.add(fringe_len)
        else:
            winner: Node = [x for x in expanded if x == board.final_state][0]
            depth = winner.depth
            display_path(winner, board)
            break

    # README INFORMATION
    if depth == -1:
        max_num = 0
        exp = 0

    # Returns necessary data to output
    return depth, max_num, exp, max(fringe_lens)


def dfs(board):
    fringe: list = [board.initial_state]
    expanded: set = {board.initial_state}

    max_num = 0
    exp = 0
    fringe_lens = {0}
    fringe_len = 1
    depth = -1

    # Visits and expands the latest added child, allowing to iteratively attempt a depth-first search
    while len(fringe) > 0:
        node = list.pop(fringe)
        if node.depth > DEPTH_LIMITS[board.size]:
            continue

        fringe_len = fringe_len - 1
        expanded.add(node)
        exp += 1
        if board.final_state != node:
            child_nodes = branch(node, board)
            child_nodes_len = len(child_nodes)
            max_num = max_num + child_nodes_len
            fringe_len = fringe_len + child_nodes_len
            for child_node in child_nodes:
                if child_node not in expanded:
                    fringe.append(child_node)
            fringe_lens.add(fringe_len)
        else:
            winner: Node = [x for x in expanded if x == board.final_state][0]
            depth = winner.depth
            display_path(winner, board)
            break
        exp += 1

    # README INFORMATION
    if depth == -1:
        max_num = 0
        exp = 0

    # Returns necessary data to output
    return depth, max_num, exp, max(fringe_lens)


def a(board):
    # Cost of first node as default value = 0
    fringe: list = [(0, board.initial_state)]
    expanded: set = {board.initial_state}

    max_num = 0
    exp = 0
    fringe_lens = {0}
    fringe_len = 1
    depth = -1

    # Attempts to farther visit and expand the node with lowest possible actual + heuristic cost
    while len(fringe) > 0:
        node_heuristic, node = fringe[0]
        fringe.remove(fringe[0])
        fringe_len = fringe_len - 1
        expanded.add(node)
        exp += 1
        if board.final_state != node:
            child_nodes = branch(node, board)
            child_nodes_len = len(child_nodes)
            max_num = max_num + child_nodes_len
            fringe_len = fringe_len + child_nodes_len
            for child_node in child_nodes:
                if child_node not in expanded:
                    fringe.append((child_node.heuristic + child_node.depth, child_node))
            fringe_lens.add(fringe_len)
            fringe.sort(key=lambda n: n[0])
        else:
            winner: Node = [x for x in expanded if x == board.final_state][0]
            depth = winner.depth
            display_path(winner, board)
            break

    # README INFORMATION
    if depth == -1:
        max_num = 0
        exp = 0

    # Returns necessary data to output
    return depth, max_num, exp, max(fringe_lens)


def greedy(board):
    # Cost of first node as default value = 0
    fringe: list = [(0, board.initial_state)]
    expanded: set = {board.initial_state}

    max_num = 0
    exp = 0
    fringe_lens = {0}
    fringe_len = 1
    depth = -1

    # Attempts to farther visit and expand the node with lowest available heuristic cost
    while len(fringe) > 0:
        node_heuristic, node = fringe[0]
        fringe.remove(fringe[0])
        fringe_len = fringe_len - 1
        expanded.add(node)
        exp += 1
        if board.final_state != node:
            child_nodes = branch(node, board)
            child_nodes_len = len(child_nodes)
            max_num = max_num + child_nodes_len
            fringe_len = fringe_len + child_nodes_len
            for child_node in child_nodes:
                if child_node not in expanded:
                    fringe.append((child_node.heuristic, child_node))
            fringe_lens.add(fringe_len)
            fringe.sort(key=lambda n: n[0])
        else:
            winner: Node = [x for x in expanded if x == board.final_state][0]
            depth = winner.depth
            display_path(winner, board)
            break

    # README INFORMATION
    if depth == -1:
        max_num = 0
        exp = 0

    # Returns necessary data to output
    return depth, max_num, exp, max(fringe_lens)
