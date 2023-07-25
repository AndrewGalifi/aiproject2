import random
import networkx as nx
from GraphGenerator import GraphGenerator
from collections import deque
import time


def main(agent_selected):
    g, agent, target, shortest_paths, observed_node, probabilities = GraphGenerator()
    target_movement_range = 1

    # step is the number of target steps, not necessarily agent steps (agent may not move when target steps into agent)
    step = 0
    while agent != target:
        neighbors = list(g.neighbors(target))
        next_node = random.choice(neighbors)
        target = next_node

        match agent_selected:
            case 0:
                pass
            case 1:
                agent = agentOneModel(agent, target, shortest_paths)
            case 2:
                agent = agentTwoModel(agent, target, g)
            case 3:
                agent = observed_node
            case 4:
                agent = agentFourModel(agent, target, g, probabilities, target_movement_range)
            case 5:
                pass
            case 6:
                agent = agentSixModel(agent, target, g, probabilities, target_movement_range, shortest_paths)
            case 7:
                pass

        step += 1
        if agent == target:
            return step


# bfs
def agentOneModel(agent, target, sp):
    agent_path = sp[agent][target]

    if len(agent_path) == 1:
        return agent_path[0]

    return agent_path[1]


# TODO
# astar, must beat number of moves
def agentTwoModel(agent, target, g):
    agent_path = nx.astar_path(g, agent, target)

    if len(agent_path) == 1:
        return agent_path[0]

    return agent_path[1]


def agentFourModel(agent, target, g, probabilities, target_movement_range):
    node_to_observe = getMostLikelyNode(probabilities)

    if target_movement_range < 40:
        target_movement_range += 1

    if node_to_observe == target:
        return target

    if node_to_observe != target:
        updateProbabilities(probabilities, node_to_observe, g, target_movement_range)
        propagateProbabilities(probabilities, g, target_movement_range)

    return agent


# TODO
# less num of examinations (compare # of examinations between a4 / reduce ways of updating probability
def agentFiveModel():
    pass


def agentSixModel(agent, target, g, probabilities, target_movement_range, sp):
    node_to_observe = getMostLikelyNode(probabilities)

    if target_movement_range < 40:
        target_movement_range += 1

    if node_to_observe == target:
        return target

    if node_to_observe != target:
        updateProbabilities(probabilities, node_to_observe, g, target_movement_range)
        propagateProbabilities(probabilities, g, target_movement_range)

    node_to_observe = getMostLikelyNode(probabilities)
    agent_path = sp[agent][node_to_observe]

    if len(agent_path) == 1:
        return agent_path[0]
    return agent_path[1]


# TODO
# same as agent six, but instead of random choice of most likely node, choose the one of shortest path (agent -->
# most likely)?

# comb of 5 and 2 (astar etc.)
def agentSevenModel():
    pass


# This sets the checked nodes probability to 0 and spreads out its old probability to the rest of the nodes in range
def updateProbabilities(probabilities, checked_node, g, target_movement_range):
    probabilities[checked_node] = 0

    nodes_in_range = getNodesInRange(g, checked_node, target_movement_range)

    for n in nodes_in_range:
        probabilities[n] += probabilities[checked_node] / len(nodes_in_range)


# Spreads out the probabilities to nearby nodes based on the target_movement_range
def propagateProbabilities(probabilities, g, target_movement_range):
    new_probs = {}

    for node, prob in probabilities.items():

        # Get nodes in movement range
        nodes_in_range = getNodesInRange(g, node, target_movement_range)

        for n in nodes_in_range:
            new_probs[n] = new_probs.get(n, 0) + prob / len(nodes_in_range)

    return new_probs


# Makes a list of the most likely nodes with the given probabilities
def getMostLikelyNode(probabilities):
    max_probability = max(probabilities.values())
    likely_nodes = [n for n, p in probabilities.items() if p == max_probability]

    return random.choice(likely_nodes)


# BFS Implementation to find nodes in range of the target_movement_range
def getNodesInRange(g, start_node, range_limit):
    visited = set()
    queue = deque([start_node])

    for x in range(range_limit):

        current = queue.popleft()
        neighbors = g.neighbors(current)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    return list(visited)


steps = []
times = []
for i in range(0, 7):
    if i != 5 and i != 7:  # for testing certain agents
        for _ in range(1, 501):
            startTime = time.time()
            steps.append(main(i))
            endTime = time.time()
            times.append(endTime - startTime)
        print(f"Average steps of Agent{i}: " + str(round(sum(steps) / 500)))
        avgTime = sum(times) / 500
        print(f"Average Time of Agent {i}: " + str(round(avgTime, 5)) + "\n")
        steps = []
        times = []
