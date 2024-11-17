import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from IPython.display import HTML


# BFS algorithm modified to capture each step
def bfs_visualization(graph, start):
    visited = [False] * len(graph)
    queue = [start]
    visited[start] = True
    steps = []  # To capture each step of BFS

    while queue:
        s = queue.pop(0)
        steps.append((list(queue), list(visited)))
        for i in graph[s]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True

    return steps


# Create graph from edges
edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (2, 5), (3, 6), (4, 6), (5, 7), (6, 7)]
G = nx.DiGraph()
G.add_edges_from(edges)

# Perform BFS and get steps
steps = bfs_visualization(G, 0)


# Function to draw the graph at each step
def draw_graph(step):
    queue, visited = step
    plt.clf()
    color_map = ["green" if visited[node] else "lightblue" for node in G]
    nx.draw(
        G,
        with_labels=True,
        node_color=color_map,
        node_size=800,
        arrowstyle="->",
        arrowsize=20,
    )
    plt.title(f"Step {steps.index(step) + 1}: Current Queue: {queue}")


# Create the animation
fig = plt.figure(figsize=(8, 6))
ani = animation.FuncAnimation(
    fig, draw_graph, frames=steps, repeat=False, interval=1000
)

# Display the animation
HTML(ani.to_html5_video())
