import networkx as nx
import numpy as np
import csv
import multiprocessing

# Parameters
n = 500
k2 = 20
initial_activated_count = 10
total_experiments = 1000
sigma = 3

# Function to update activation status with transmission based on state
def spread_activation(G, node_states, k1, k2, sigma):
    new_fully_activated = set()
    new_weakly_activated = set()
    direct_full_activation = 0

    for node in G.nodes:
        if node_states[node] == 0 or node_states[node] == 1:
            neighbors = set(G.neighbors(node))
            transmission_sum = sum(sigma if node_states[neighbor] == sigma else 1 if node_states[neighbor] == 1 else 0 for neighbor in neighbors)

            if transmission_sum >= k2:
                new_fully_activated.add(node)
                if node_states[node] == 0:
                    direct_full_activation += 1
            elif k1 is not None and transmission_sum >= k1:
                new_weakly_activated.add(node)

    for node in new_fully_activated:
        node_states[node] = sigma
    for node in new_weakly_activated:
        node_states[node] = 1

    return new_fully_activated, new_weakly_activated, direct_full_activation

# Single experiment function for parallel execution
def single_experiment(k1, p):
    G = nx.erdos_renyi_graph(n, p)
    initial_activated = np.random.choice(G.nodes, initial_activated_count, replace=False)
    node_states = {node: sigma if node in initial_activated else 0 for node in G.nodes}

    previous_fully_activated_count = sum(1 for state in node_states.values() if state == sigma)
    previous_weakly_activated_count = sum(1 for state in node_states.values() if state == 1)
    penultimate_weak_activation_proportion = 0
    final_activation_occurred = False

    iteration_count = 0
    direct_full_activation_count = 0
    first_step_weak_count = 0
    first_step_full_count = 0
    final_step_full_activation_proportion = 0

    while True:
        new_fully_activated, new_weakly_activated, direct_full_activation = spread_activation(G, node_states, k1, k2, sigma)

        if iteration_count == 0:
            first_step_weak_count = len(new_weakly_activated)
            first_step_full_count = len(new_fully_activated)

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

    direct_full_activation_ratio = direct_full_activation_count / (current_fully_activated_count - initial_activated_count) if current_fully_activated_count > initial_activated_count else 0
    fully_activated = current_fully_activated_count
    weakly_activated = current_weakly_activated_count
    full_activation = current_fully_activated_count == n
    return fully_activated, weakly_activated, iteration_count, direct_full_activation_ratio, penultimate_weak_activation_proportion, first_step_weak_count, first_step_full_count, final_step_full_activation_proportion, full_activation

# Function to run all experiments in parallel for a given k1 and p
def parallel_experiments(k1, p):
    with multiprocessing.Pool(processes=32) as pool:  # Specify the number of cores to use
        results = pool.starmap(single_experiment, [(k1, p) for _ in range(total_experiments)])

    fully_activated_counts = [result[0] for result in results]
    weakly_activated_counts = [result[1] for result in results]
    iteration_counts = [result[2] for result in results]
    direct_full_activation_ratios = [result[3] for result in results if result[3] > 0]
    penultimate_weak_activation_proportions = [result[4] for result in results if result[4] > 0]
    first_step_weak_counts = [result[5] for result in results]
    first_step_full_counts = [result[6] for result in results]
    final_step_full_activation_proportions = [result[7] for result in results]
    full_activation_count = sum(result[8] for result in results)

    average_fully_activated = np.mean(fully_activated_counts)
    average_weakly_activated = np.mean(weakly_activated_counts)
    full_activation_proportion = full_activation_count / total_experiments
    average_iterations_for_full_activation = np.mean([count for count, fully in zip(iteration_counts, fully_activated_counts) if fully == n]) if full_activation_proportion > 0 else 0
    average_direct_full_activation_ratio = np.mean(direct_full_activation_ratios) if direct_full_activation_ratios else 0
    average_penultimate_weak_activation_proportion = np.mean(penultimate_weak_activation_proportions) if penultimate_weak_activation_proportions else 0
    average_first_step_weak_count = np.mean(first_step_weak_counts) if first_step_weak_counts else 0
    average_first_step_full_count = np.mean(first_step_full_counts) if first_step_full_counts else 0
    average_final_step_full_activation_proportion = np.mean(final_step_full_activation_proportions)

    return [k1, k2, n, p, total_experiments, sigma, average_fully_activated, average_weakly_activated, full_activation_proportion,
            average_iterations_for_full_activation, average_direct_full_activation_ratio, average_penultimate_weak_activation_proportion,
            average_first_step_weak_count, average_first_step_full_count, average_final_step_full_activation_proportion]

# Write results to CSV
if __name__ == '__main__':
    with open('parallel2.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['k1', 'k2', 'n', 'p', 'Total Experiments', 'sigma', 'Average Fully Activated Nodes',
                         'Average Weakly Activated Nodes', 'Full Activation Proportion', 'Average Iterations for Full Activation',
                         'Average Direct Full Activation Proportion', 'Penultimate Weak Activation Proportion',
                         'First Step Weak Activation Count', 'First Step Full Activation Count', 'Final Step Full Activation Proportion'])

        for k1 in [None] + list(range(3, 20)):
            for p in np.arange(0, 1.02, 0.02):
                result = parallel_experiments(k1, p)
                writer.writerow(result)
                print(f"k1: {k1}, p: {p:.2f}, Result: {result}")
