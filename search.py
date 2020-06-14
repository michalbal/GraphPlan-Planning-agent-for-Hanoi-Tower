"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


class Node:
    def __init__(self, state, cost, path, action=None):
        self.state = state
        self.cost = cost
        if action is not None:
            self.path = path + [action]
        else:
            self.path = path


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    # DFS is LIFO
    fringe = util.Stack()
    fringe.push([problem.get_start_state(), None])  # board
    visited = set()
    path = []
    depth = [1]
    while not fringe.isEmpty():
        current, move = fringe.pop()  # get board
        if move is not None:
            while depth[-1] == 0:
                # delete last elements of the path
                path.__delitem__(-1)
                depth.__delitem__(-1)
            depth[-1] -= 1
            path[-1] = move
        # also deleted from fringe

        if problem.is_goal_state(current):
            return path
        elif not current in visited:  # set of states of board
            visited.add(current)
            successors = problem.get_successors(current)
            if len(successors) == 0:
                continue  # no successors
            depth.append(len(successors))
            path.append(None)
            for successor in reversed(
                    successors):  # change to "successors:" for better pacman
                fringe.push([successor[0], successor[1]])
    # no path
    return []


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # BFS is FIFO
    fringe = util.Queue()
    fringe.push([problem.get_start_state(), []])  # board
    visited = set()  # for now
    while not fringe.isEmpty():
        current, move = fringe.pop()  # get board
        if problem.is_goal_state(current):
            return move
        elif not current in visited:  # set of states of board
            visited.add(current)
            successors = problem.get_successors(current)
            for successor in reversed(successors):
                fringe.push([successor[0], move + [successor[1]]])
    # no path
    return []


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    fringe = util.PriorityQueue()
    visited = set()
    first_state = problem.get_start_state()
    fringe.push(Node(first_state, 0, []), 0)
    while not fringe.isEmpty():
        current_node = fringe.pop()
        if not current_node.state in visited:
            if problem.is_goal_state(current_node.state):
                return current_node.path
            # Expand node
            visited.add(current_node.state)
            successors = problem.get_successors(current_node.state)
            # successors.reverse()
            for succ, action, cost in successors:
                # if succ in visited:
                #     continue
                accumulated_cost = current_node.cost + cost
                fringe.push(
                    Node(succ, accumulated_cost, current_node.path, action),
                    accumulated_cost)
    return []


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    visited = set()
    first_state = problem.get_start_state()
    fringe.push(Node(first_state, 0, []), 0)
    while not fringe.isEmpty():
        current_node = fringe.pop()
        if not current_node.state in visited:
            if problem.is_goal_state(current_node.state):
                return current_node.path
            # Expand node
            visited.add(current_node.state)
            successors = problem.get_successors(current_node.state)
            # successors.reverse()
            for succ, action, cost in successors:
                # if succ in visited:
                #     continue
                accumulated_cost = current_node.cost + cost
                heuristic_cost = heuristic(succ, problem)
                fringe.push(
                    Node(succ, accumulated_cost, current_node.path, action),
                    accumulated_cost + heuristic_cost)
    return None


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
