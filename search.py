# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do NOT need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    start = problem.getStartState()

    # LIFO
    stack = util.Stack()
    #Node: State; Action, Cost
    stack.push((start, [], 0))

    #Set of visited nodes
    #Keys State; Values: Actions
    explored = {}

    #Loop while there are still frontiers
    while not stack.isEmpty():
        # Last node entered
        node = stack.pop()
        # Make sure state not visited
        if node[0] not in explored.keys():
            #Mark it as visited
            explored[node[0]] = node[1]
            # Check it reach out Goal State
            if problem.isGoalState(node[0]):
                return node[1]

            #Loop through all successors from last node entered
            for nextState, nextAction, nextCost in  problem.getSuccessors(node[0]):
                newNode = (nextState, node[1] + [nextAction], nextCost)
                #Add Node in stack
                stack.push(newNode)
    
    return node[1]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    "*** YOUR CODE HERE ***"

    start = problem.getStartState()

    #FIFO
    queue = util.Queue()
    #Node: State; Action, Cost
    queue.push((start, [], 0))

    #Set of visited nodes
    #Keys State; Values: Actions
    explored = []
    
    #Loop while there are still frontiers
    while not queue.isEmpty():
        # First node entered
        node = queue.pop()
        # Make sure state not visited
        if node[0] not in explored:
            #Mark it as visited
            explored.append(node[0])
            # Check it reach out Goal State
            if problem.isGoalState(node[0]):
                return node[1]

            #Loop through all successors from current node 
            for nextState, nextAction, nextCost in  problem.getSuccessors(node[0]):
                newNode = (nextState, node[1] + [nextAction], nextCost)
                #Add Node in stack
                queue.push(newNode)
    
    return node[1]


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    #FIFO based on priority. Here cost
    priorityQueue = util.PriorityQueue()
    #Node: State; Action, Cost 
    priorityQueue.push((start, [], 0), 0)

    #Set of visited nodes
    #Keys State; Values: Cost
    explored = []

    #Loop while there are still frontiers
    while not priorityQueue.isEmpty():
        # First node with least cost
        node = priorityQueue.pop()
        # Make sure node not visited and that its cost is less
        if (node[0] not in explored):
            # Mark node
            explored.append(node[0])
            # Check it reach out Goal State
            if problem.isGoalState(node[0]):
                return node[1]

            #Loop through all successors from current node 
            for nextState, nextAction, nextCost in  problem.getSuccessors(node[0]):
                newNode = (nextState, node[1] + [nextAction],  node[2] + nextCost)
                #Add Node in stack with the path cost
                priorityQueue.update(newNode, node[2] + nextCost)
    
    return node[1]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #FIFO based on priority. Here cost
    priorityQueue = util.PriorityQueue()
    #Node: State; Action, Cost 
    priorityQueue.push((start, [], 0), heuristic(start, problem))

    #Set of visited nodes
    #Keys State; Values: Cost
    explored = []

    #Loop while there are still frontiers
    while not priorityQueue.isEmpty():
        # First node with least cost
        node = priorityQueue.pop()
        # Check it reach out Goal State
        if problem.isGoalState(node[0]):
            return node[1]
        # Make sure node not visited
        if node[0] not in explored:
            # Mark node
            explored.append(node[0])

            #Loop through all successors from current node 
            for nextState, nextAction, nextCost in problem.getSuccessors(node[0]):
                if nextState not in explored:
                    # Cost of the path about to take
                    pathCost = problem.getCostOfActions(node[1] + [nextAction])
                    # Heuristic differentiate A* and UCS 
                    newCost = heuristic(nextState, problem)
                    newNode = (nextState, node[1] + [nextAction], nextCost)
                    #Add Node in stack with the path cost
                    priorityQueue.update(newNode, pathCost + newCost)
        
    return node[1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
