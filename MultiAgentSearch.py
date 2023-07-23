import random
from GraphGenerator import GraphGenerator
from collections import deque


def main(agent_selected):
    g, agent, target, shortest_paths, observed_node, probabilities = GraphGenerator()
    target_movement_range = 1

    # print("Enter agent number (0-4) to simulate:")
    # agent_selected = int(input())

    # step is number of target steps, not necessarily agent steps (agent may not move when target steps into agent)
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
                pass
            case 3:
                agent = observed_node
            case 4:
                agent = agentFourModel(agent, target, g, probabilities, target_movement_range)

        step += 1
        if agent == target:
            # print(f"S{step}:\nAgent found Target at node {target}")
            return step
            # break

        # print(f"S{step}: Target is at node {target},\nS{step}: Agent is at node {agent}\n")


def agentOneModel(agent, target, sp):
    agent_path = sp[agent][target]

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
for i in range(0, 5):
    for _ in range(1, 51):
        steps.append(main(i))
    print(f"Average steps of Agent{i}: " + str(round(sum(steps) / 50)))
    steps = []
