import random
import networkx as nx


def GraphGenerator():
    # Create graph with 40 nodes
    g = nx.Graph()
    for i in range(1, 41):
        g.add_node(i)

    # Connect nodes in a loop
    for i in range(1, 40):
        g.add_edge(i, i + 1)
        g.add_edge(40, 1)

    num_edges_added = 0
    while num_edges_added < 10:
        u = random.randint(1, 40)
        v = random.randint(1, 40)

        if u != v and not g.has_edge(u, v):
            g.add_edge(u, v)
            # print(f"Added edge: ({u}, {v})")
            num_edges_added += 1

    # Initialize target and agent at random node
    target = random.randint(1, 40)
    agent = random.randint(1, 40)
    while agent == target:
        agent = random.randint(1, 40)

    # nx.draw(g, with_labels=True)
    # plt.savefig("graph.png")

    shortest_paths = dict(nx.all_pairs_shortest_path(g))

    return g, agent, target, shortest_paths
