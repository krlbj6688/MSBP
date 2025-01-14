import networkx as nx
import numpy as np
import csv

# Parameters
k1 = 13  # Fixed k1 value
k2 = 20  # Total transmitted value required for full activation
initial_activated_count = 10  # Number of initial activated nodes
total_experiments = 1000  # Total number of experiments for each p
sigma = 3  # Transmission value for fully activated nodes
n_values = range(500, 10001, 500)  # Node counts from 500 to 10000 with a step of 500

# Function to update activation status with transmission based on state
def spread_activation(G, node_states, k1, k2, sigma):
    new_fully_activated = set()
    new_weakly_activated = set()
    direct_full_activation = 0

    for node in G.nodes:
        if node_states[node] in [0, 1]:
            neighbors = set(G.neighbors(node))
            transmission_sum = sum(sigma if node_states[neighbor] == sigma else 1 if node_states[neighbor] == 1 else 0 for neighbor in neighbors)

            if transmission_sum >= k2:
                new_fully_activated.add(node)
                if node_states[node] == 0:
                    direct_full_activation += 1
            #elif transmission_sum >= k1:
            elif transmission_sum >= k1 and node_states[node] != 1:
                new_weakly_activated.add(node)

    for node in new_fully_activated:
        node_states[node] = sigma
    for node in new_weakly_activated:
        node_states[node] = 1

    return new_fully_activated, new_weakly_activated, direct_full_activation


# Open a CSV file to write results
with open('activation_process_n_values.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the CSV header
    writer.writerow(['n', 'k1', 'k2', 'p', 'Total Experiments', 'sigma', 'Average Fully Activated Nodes',
                     'Average Weakly Activated Nodes', 'Full Activation Proportion', 'Average Iterations for Full Activation',
                     'Average Direct Full Activation Proportion', 'Penultimate Weak Activation Proportion',
                     'First Step Weak Activation Count', 'First Step Full Activation Count', 'Final Step Full Activation Proportion'])

    # Iterate over n values
    for n in n_values:
        # Iterate over p values
        for p in np.arange(0, 1.02, 0.02):
            fully_activated_counts = []
            weakly_activated_counts = []
            full_activation_count = 0
            total_iterations_for_full_activation = 0
            direct_full_activation_ratios = []
            penultimate_weak_activation_proportions = []
            first_step_weak_counts = []
            first_step_full_counts = []
            final_step_full_activation_proportions = []

            # Run experiments for each p value
            for _ in range(total_experiments):
                G = nx.erdos_renyi_graph(n, p)

                initial_activated = np.random.choice(G.nodes, initial_activated_count, replace=False)
                node_states = {node: sigma if node in initial_activated else 0 for node in G.nodes}

                previous_fully_activated_count = sum(1 for state in node_states.values() if state == sigma)
                previous_weakly_activated_count = sum(1 for state in node_states.values() if state == 1)
                penultimate_weak_activation_proportion = 0
                final_step_full_activation_proportion = 0
                final_activation_occurred = False

                iteration_count = 0
                direct_full_activation_count = 0

                # Spread activation until no more changes
                while True:
                    new_fully_activated, new_weakly_activated, direct_full_activation = spread_activation(G, node_states, k1, k2, sigma)

                    if iteration_count == 0:
                        first_step_weak_counts.append(len(new_weakly_activated))
                        first_step_full_counts.append(len(new_fully_activated))

                    current_fully_activated_count = sum(1 for state in node_states.values() if state == sigma)
                    current_weakly_activated_count = sum(1 for state in node_states.values() if state == 1)

                    if len(new_fully_activated) > 0 or len(new_weakly_activated) > 0:
                        final_activation_occurred = True
                        penultimate_weak_activation_proportion = previous_weakly_activated_count / n
                        final_step_full_activation_proportion = len(new_fully_activated) / n

                    if (current_fully_activated_count == previous_fully_activated_count and
                        current_weakly_activated_count == previous_weakly_activated_count):
                        break

                    iteration_count += 1
                    previous_fully_activated_count = current_fully_activated_count
                    previous_weakly_activated_count = current_weakly_activated_count
                    direct_full_activation_count += direct_full_activation

                if current_fully_activated_count > initial_activated_count:
                    direct_full_activation_ratio = direct_full_activation_count / (current_fully_activated_count - initial_activated_count)
                    direct_full_activation_ratios.append(direct_full_activation_ratio)

                if current_fully_activated_count == n:
                    full_activation_count += 1
                    total_iterations_for_full_activation += iteration_count

                if final_activation_occurred:
                    penultimate_weak_activation_proportions.append(penultimate_weak_activation_proportion)
                    final_step_full_activation_proportions.append(final_step_full_activation_proportion)

                fully_activated_counts.append(current_fully_activated_count)
                weakly_activated_counts.append(current_weakly_activated_count)

            average_fully_activated = np.mean(fully_activated_counts)
            average_weakly_activated = np.mean(weakly_activated_counts)
            full_activation_proportion = full_activation_count / total_experiments
            average_iterations_for_full_activation = (total_iterations_for_full_activation / full_activation_count) if full_activation_count > 0 else 0
            average_direct_full_activation_ratio = np.mean(direct_full_activation_ratios) if direct_full_activation_ratios else 0
            average_penultimate_weak_activation_proportion = np.mean(penultimate_weak_activation_proportions) if penultimate_weak_activation_proportions else 0
            average_first_step_weak_count = np.mean(first_step_weak_counts) if first_step_weak_counts else 0
            average_first_step_full_count = np.mean(first_step_full_counts) if first_step_full_counts else 0
            average_final_step_full_activation_proportion = np.mean(final_step_full_activation_proportions) if final_step_full_activation_proportions else 0

            writer.writerow([n, k1, k2, p, total_experiments, sigma, average_fully_activated,
                             average_weakly_activated, full_activation_proportion, average_iterations_for_full_activation,
                             average_direct_full_activation_ratio, average_penultimate_weak_activation_proportion,
                             average_first_step_weak_count, average_first_step_full_count,
                             average_final_step_full_activation_proportion])
