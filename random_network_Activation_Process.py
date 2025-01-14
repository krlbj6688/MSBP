import networkx as nx
import numpy as np
import csv

# Parameters
n = 500  # Number of nodes
k2 = 20  # Total transmitted value required for full activation
initial_activated_count = 10  # Number of initial activated nodes
total_experiments = 1000  # Total number of experiments for each p
sigma = 3  # Transmission value for fully activated nodes

# Function to update activation status with transmission based on state
def spread_activation(G, node_states, k1, k2, sigma):
    new_fully_activated = set()
    new_weakly_activated = set()
    direct_full_activation = 0  # Count nodes that go from inactive (0) directly to fully activated (sigma)

    for node in G.nodes:
        if node_states[node] == 0 or node_states[node] == 1:  # Consider non-activated and weakly activated nodes
            neighbors = set(G.neighbors(node))
            # Sum transmission values from neighbors (fully activated: sigma, weakly activated: 1)
            transmission_sum = sum(sigma if node_states[neighbor] == sigma else 1 if node_states[neighbor] == 1 else 0 for neighbor in neighbors)

            if transmission_sum >= k2:
                new_fully_activated.add(node)
                if node_states[node] == 0:  # Check if the node was previously inactive (0)
                    direct_full_activation += 1
            elif k1 is not None and transmission_sum >= k1:  # If k1 is defined, check for weak activation
                new_weakly_activated.add(node)

    # Update states: sigma for fully activated, 1 for weakly activated
    for node in new_fully_activated:
        node_states[node] = sigma
    for node in new_weakly_activated:
        node_states[node] = 1

    return new_fully_activated, new_weakly_activated, direct_full_activation


# Open a CSV file to write results
with open('with_penultimate_weak_proportion.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the CSV header
    writer.writerow(['k1', 'k2', 'n', 'p', 'Total Experiments', 'Average Fully Activated Nodes',
                     'Average Weakly Activated Nodes', 'Full Activation Proportion', 'Average Iterations for Full Activation',
                     'Average Direct Full Activation Proportion', 'Penultimate Weak Activation Proportion'])

    # Iterate over k1 values
    for k1 in [None] + list(range(3, 16)):
        # Iterate over p values
        for p in np.arange(0, 1.02, 0.02):
            fully_activated_counts = []
            weakly_activated_counts = []
            full_activation_count = 0  # Count how many times all nodes are fully activated
            total_iterations_for_full_activation = 0  # Track total iterations for experiments that reach full activation
            direct_full_activation_ratios = []  # List to store direct full activation ratios for each experiment
            penultimate_weak_activation_proportions = []  # List to store penultimate weak activation proportion

            # Run experiments for each p value
            for _ in range(total_experiments):
                # Generate the random network
                G = nx.erdos_renyi_graph(n, p)

                # Initialize activated nodes
                initial_activated = np.random.choice(G.nodes, initial_activated_count, replace=False)
                node_states = {node: sigma if node in initial_activated else 0 for node in G.nodes}  # State: 0 (inactive), 1 (weak), sigma (full)

                previous_fully_activated_count = sum(1 for state in node_states.values() if state == sigma)
                previous_weakly_activated_count = sum(1 for state in node_states.values() if state == 1)
                penultimate_weak_activation_proportion = 0
                final_activation_occurred = False  # Flag to track if there were new activations in the final step

                iteration_count = 0  # Track the number of iterations
                direct_full_activation_count = 0  # Track nodes that go directly from 0 to sigma

                # Spread activation until no more changes
                while True:
                    new_fully_activated, new_weakly_activated, direct_full_activation = spread_activation(G, node_states, k1, k2, sigma)

                    current_fully_activated_count = sum(1 for state in node_states.values() if state == sigma)
                    current_weakly_activated_count = sum(1 for state in node_states.values() if state == 1)

                    # Check if new activations occurred
                    if len(new_fully_activated) > 0 or len(new_weakly_activated) > 0:
                        final_activation_occurred = True  # Mark that new activations occurred in this step
                        # Store the current weak activation proportion as the penultimate weak activation proportion
                        penultimate_weak_activation_proportion = previous_weakly_activated_count / n

                    # Check if the activation spread has stopped
                    if (current_fully_activated_count == previous_fully_activated_count and
                            current_weakly_activated_count == previous_weakly_activated_count):
                        break

                    iteration_count += 1  # Increment iteration count for each spread

                    previous_fully_activated_count = current_fully_activated_count
                    previous_weakly_activated_count = current_weakly_activated_count

                    direct_full_activation_count += direct_full_activation  # Accumulate direct full activation count

                # Calculate the proportion of direct full activation for this experiment
                if current_fully_activated_count > initial_activated_count:
                    direct_full_activation_ratio = direct_full_activation_count / (current_fully_activated_count - initial_activated_count)
                    direct_full_activation_ratios.append(direct_full_activation_ratio)

                # Check if all nodes are fully activated
                if current_fully_activated_count == n:
                    full_activation_count += 1  # Increment the count if all nodes are fully activated
                    total_iterations_for_full_activation += iteration_count  # Add the number of iterations for this experiment

                # Store the penultimate weak activation proportion only if final activation occurred
                if final_activation_occurred:
                    penultimate_weak_activation_proportions.append(penultimate_weak_activation_proportion)

                # Store the results for this experiment
                fully_activated_counts.append(current_fully_activated_count)
                weakly_activated_counts.append(current_weakly_activated_count)

            # Calculate averages for this p
            average_fully_activated = np.mean(fully_activated_counts)
            average_weakly_activated = np.mean(weakly_activated_counts)

            # Calculate the proportion of experiments where all nodes were fully activated
            full_activation_proportion = full_activation_count / total_experiments

            # Calculate average iterations for full activation
            if full_activation_count > 0:
                average_iterations_for_full_activation = total_iterations_for_full_activation / full_activation_count
            else:
                average_iterations_for_full_activation = 0

            # Calculate the average direct full activation ratio
            if direct_full_activation_ratios:
                average_direct_full_activation_ratio = np.mean(direct_full_activation_ratios)
            else:
                average_direct_full_activation_ratio = 0

            # Calculate average penultimate weak activation proportion
            if penultimate_weak_activation_proportions:
                average_penultimate_weak_activation_proportion = np.mean(penultimate_weak_activation_proportions)
            else:
                average_penultimate_weak_activation_proportion = 0

            # Write the results to the CSV file
            writer.writerow([k1, k2, n, p, total_experiments, average_fully_activated,
                             average_weakly_activated, full_activation_proportion, average_iterations_for_full_activation,
                             average_direct_full_activation_ratio, average_penultimate_weak_activation_proportion])

            # Output the results for this k1 and p
            print(f"k1: {k1}, p: {p:.2f}, Average Fully Activated Nodes: {average_fully_activated}, "
                  f"Average Weakly Activated Nodes: {average_weakly_activated}, "
                  f"Full Activation Proportion: {full_activation_proportion:.2f}, "
                  f"Average Direct Full Activation Ratio: {average_direct_full_activation_ratio:.2f}, "
                  f"Penultimate Weak Activation Proportion: {average_penultimate_weak_activation_proportion:.2f}, "
                  f"Average Iterations for Full Activation: {average_iterations_for_full_activation:.2f}")
