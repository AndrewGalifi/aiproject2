import random
import networkx as nx
from GraphGenerator import GraphGenerator
from collections import deque
import time


def main(agent_selected):
    g, agent, target, shortest_paths, observed_node, probabilities = GraphGenerator()

    target_movement_range = [1]

    step = 0
    while agent != target:
        neighbors = list(g.neighbors(target))
        next_node = random.choice(neighbors)
        target = next_node
        no_step = False

        match agent_selected:
            case 0:
                pass
            case 1:
                agent, no_step = agentOneModel(agent, target, g)
            case 2:
                agent, no_step = agentTwoModel(agent, target, g, shortest_paths)
            case 3:
                agent = observed_node
            case 4:
                agent, probabilities = agentFourModel(agent, target, g, probabilities, target_movement_range)
            case 5:
                agent, probabilities = agentFiveModel(agent, target, g, probabilities, target_movement_range)
            case 6:
                agent, probabilities = agentSixModel(agent, target, g, probabilities, target_movement_range, shortest_paths)
            case 7:
                pass

        if no_step:
            step -= 1

        step += 1

        if agent == target:
            return step


# bfs
def agentOneModel(agent, target, g):
    agent_path = nx.dijkstra_path(g, agent, target)

    no_step = False

    if len(agent_path) == 1:
        no_step = True
        return agent_path[0], no_step

    return agent_path[1], no_step


# TODO
# astar, must beat number of moves
def agentTwoModel(agent, target, g, sp):
    def distance(a, t):
        return len(sp[a][t])-1

    agent_path = nx.astar_path(g, agent, target, heuristic=distance)

    no_step = False

    if len(agent_path) == 1:
        no_step = True
        return agent_path[0], no_step

    return agent_path[1], no_step


def agentFourModel(agent, target, g, probabilities, target_movement_range):
    node_to_observe = getMostLikelyNode(probabilities)

    if node_to_observe == target:
        return target, probabilities

    if node_to_observe != target:
        updateProbabilities(probabilities, node_to_observe, g, target_movement_range[0])
        propagateProbabilities(probabilities, g, target_movement_range[0])

    return agent, probabilities


# TODO
# less num of examinations (compare # of examinations between a4 / reduce ways of updating probability
def agentFiveModel(agent, target, g, probabilities, target_movement_range):
    node_to_observe = getMostLikelyNode(probabilities)

    if node_to_observe == target:
        return target, probabilities

    if node_to_observe != target:
        target_movement_range[0] = 1

        spreading_probability = probabilities[target] / target_movement_range[0]

        nodes_in_range = getNodesInRange(g, target, target_movement_range[0])
        for node in nodes_in_range:
            probabilities[node] += spreading_probability

        probabilities[target] = 0

        propagateProbabilities(probabilities, g, target_movement_range[0])

    # if node_to_observe != target:
    #    updateProbabilities(probabilities, node_to_observe, g, target_movement_range[0])
    #    propagateProbabilities(probabilities, g, target_movement_range[0])

    return agent, probabilities


def agentSixModel(agent, target, g, probabilities, target_movement_range, sp):
    node_to_observe = getMostLikelyNode(probabilities)

    if node_to_observe == target:
        return target, probabilities

    if node_to_observe != target:
        updateProbabilities(probabilities, node_to_observe, g, target_movement_range[0])
        propagateProbabilities(probabilities, g, target_movement_range[0])

    node_to_observe = getMostLikelyNode(probabilities)

    agent_path = sp[agent][node_to_observe]

    if len(agent_path) == 1:
        return agent_path[0], probabilities
    return agent_path[1], probabilities


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
target_movement_range = [1]
for i in range(0, 7):
    if i != 7:  # for testing certain agents
        for _ in range(1, 501):
            startTime = time.time()
            steps.append(main(i))
            endTime = time.time()
            times.append(endTime - startTime)
        print(f"Average steps of Agent {i}: " + str(round(sum(steps) / 500)))
        avgTime = sum(times) / 500
        print(f"Average time of Agent  {i}: " + str(round(avgTime, 5)) + "\n")
        steps = []
        times = []
