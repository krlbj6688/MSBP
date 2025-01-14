import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
n = 1000  # Number of nodes
k2 = 10  # Total transmission required for full activation
initial_activated_count = 10  # Number of initially activated nodes
sigma = 3  # Transmission value for fully activated nodes
p = 0.2  # Edge creation probability
k1 = 4  # Transmission required for partial activation

# Set random seed for reproducibility
#np.random.seed(42)

# Generate random network
G = nx.erdos_renyi_graph(n, p)

# Initialize node states: 0 (inactive), 1 (partially activated), sigma (fully activated)
initial_activated = np.random.choice(G.nodes, initial_activated_count, replace=False)
node_states = {node: sigma if node in initial_activated else 0 for node in G.nodes}


# Function to update activation status
def spread_activation(G, node_states, k1, k2, sigma):
    new_fully_activated = set()
    new_weakly_activated = set()

    for node in G.nodes:
        if node_states[node] == 0 or node_states[node] == 1:  # Only consider inactive and partially activated nodes
            neighbors = set(G.neighbors(node))
            # Calculate total transmission from neighbors (fully activated: sigma, partially activated: 1, inactive: 0)
            transmission_sum = sum(
                sigma if node_states[neighbor] == sigma else 1 if node_states[neighbor] == 1 else 0 for neighbor in
                neighbors)

            if transmission_sum >= k2:
                new_fully_activated.add(node)
            elif k1 is not None and transmission_sum >= k1:  # If k1 threshold met, partial activation
                new_weakly_activated.add(node)

    # Update node states: sigma for fully activated, 1 for partially activated
    for node in new_fully_activated:
        node_states[node] = sigma
    for node in new_weakly_activated:
        node_states[node] = 1

    return new_fully_activated, new_weakly_activated


# Create animation
fig, ax = plt.subplots(figsize=(8, 8))
pos = nx.circular_layout(G)  # Circular layout for nodes

# Store previous node states for comparison
previous_node_states = node_states.copy()

# Initialize iteration count
iteration_count = 0


# Generator function to yield frames for the animation
def frame_gen():
    global node_states, previous_node_states, iteration_count
    num = 0
    # Yield initial state (Step 0)
    yield num  # This will draw the initial state

    while True:
        new_fully_activated, new_weakly_activated = spread_activation(G, node_states, k1, k2, sigma)

        # Check if the activation spread has stopped
        if node_states == previous_node_states:
            print(f"Total iterations: {iteration_count}")  # Print the total iterations when it stops
            break  # Stop the generator when there are no more updates
        else:
            previous_node_states = node_states.copy()  # Update previous state for the next step
            iteration_count += 1  # Increment iteration count

        num += 1
        yield num  # Yield the current frame number


# Update function for each frame in the animation
def update(num):
    global node_states, previous_node_states, iteration_count

    # Clear the current plot
    ax.clear()
    colors = ['red' if node_states[node] == sigma else 'orange' if node_states[node] == 1 else 'lightblue' for node in
              G.nodes]
    nx.draw(G, pos, node_color=colors, with_labels=False, node_size=50, edge_color='gray', ax=ax)

    # Calculate the number of fully activated and weakly activated nodes
    fully_activated_count = sum(1 for state in node_states.values() if state == sigma)
    weakly_activated_count = sum(1 for state in node_states.values() if state == 1)

    # Add parameter information at the top of the plot
    ax.text(0.5, 1.07, f"Step {num} | Fully Activated: {fully_activated_count} | Weakly Activated: {weakly_activated_count}",
            horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12)

    # Add another line for parameters slightly lower to avoid overlap
    ax.text(0.5, 0.97, f"n={n}, k1={k1}, k2={k2}, sigma={sigma}, p={p}",
            horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=11)

    ax.set_title(f"Activation Process", fontsize=14)


# Create animation using dynamic frames from the frame generator
ani = animation.FuncAnimation(fig, update, frames=frame_gen, interval=2000, repeat=False)

# Save animation as video file
ani.save("activation_process_test.mp4", writer='ffmpeg', fps=0.5)

plt.show()
