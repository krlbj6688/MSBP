import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Parameters
n = 500  # Total number of nodes in the network
initial_activated_count = 10  # Number of initial activated nodes

# Function to check if a scenario achieves full activation
def check_full_activation(df, n):
    """
    Check if any scenario achieves full activation (all nodes activated).

    Parameters:
    df (DataFrame): Filtered data for specific k1 and p.
    n (int): Total number of nodes.

    Returns:
    dict: Scenario IDs and time steps where full activation occurs.
    """
    full_activation = {}
    for col in df.columns[7:]:  # Skip 'Time Step', 'k1', 'p' columns
        cumulative_sum = df[col].cumsum()  # Compute the cumulative sum for each scenario
        time_step = (cumulative_sum >= (n - initial_activated_count)).idxmax()  # Find the first time step where cumulative sum >= n - initial_activated_count
        if cumulative_sum[time_step] >= (n - initial_activated_count):
            full_activation[col] = time_step  # Record the scenario and the time step

    return full_activation


# Load the activation data
df = pd.read_csv('activation_fully_activated2.csv')

# Filter data for a specific k1 and p (example: k1=10, p=0.12)
k1 = 17
p = 0.46
filtered_df = df[(df['k1'] == k1) & (df['p'] == p)]

# Check for full activation
full_activation_scenarios = check_full_activation(filtered_df, n)

# Plot scenarios with full activation
if full_activation_scenarios:
    # Group scenarios by the total time steps to achieve full activation
    grouped_scenarios = {}
    for scenario, time_step in full_activation_scenarios.items():
        final_time_step = filtered_df.loc[time_step, 'Time Step']
        if final_time_step not in grouped_scenarios:
            grouped_scenarios[final_time_step] = []
        grouped_scenarios[final_time_step].append(scenario)

    # Assign colors to each group of scenarios
    unique_time_steps = sorted(grouped_scenarios.keys())  # Sort time steps to ensure legend is in ascending order
    color_map = cm.get_cmap('tab10', len(unique_time_steps))  # Generate a unique color for each group

    plt.figure(figsize=(10, 6))
    for i, final_time_step in enumerate(unique_time_steps):  # Iterate in sorted order of time steps
        color = color_map(i)  # Assign a color based on the group
        scenarios = grouped_scenarios[final_time_step]
        for scenario in scenarios:
            plt.plot(filtered_df['Time Step'], filtered_df[scenario], color=color, alpha=0.6)  # Use same color for all scenarios in group
        # Add a single entry to the legend for this time step
        plt.plot([], [], label=f"Full at Step {final_time_step}", color=color)

    # Add labels and legend
    plt.title(f'Activation Spread (k1={k1}, p={p})')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Activated Nodes (This Step)')
    plt.xlim(1, max(unique_time_steps) + 2)  # Adjust x-axis range dynamically
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    plt.tight_layout()
    plt.show()
else:
    print("No scenarios to plot, as no full activation was achieved.")
