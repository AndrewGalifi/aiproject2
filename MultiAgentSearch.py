import random
from GraphGenerator import GraphGenerator


def main():
    g, agent, target, shortest_paths, observed_node = GraphGenerator()

    print("Enter agent number (0-3) to simulate:")
    agent_selected = int(input())

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
                pass

        step += 1
        if agent == target:
            print(f"S{step}:\nAgent found Target at node {target}")
            break
        

        # print(f"S{step}: Target is at node {target},\nS{step}: Agent is at node {agent}\n")


def agentOneModel(agent, target, sp):
    agent_path = sp[agent][target]

    if len(agent_path) == 1:
        return agent_path[0]

    return agent_path[1] 

main()
