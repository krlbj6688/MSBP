import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
data = pd.read_csv('parallelF.csv')

# Replace NaN (None) values in k1 with a string "None"
data['k1'] = data['k1'].fillna('None')

# Get unique k1 values
k1_values = data['k1'].unique()

# Extract k2 and total experiments from the data
k2_value = data['k2'].unique()[0]  # Assuming k2 is constant across all rows
experiments = data['Total Experiments'].unique()[0]  # Assuming total experiments is constant
n = data['n'].unique()[0]

# Create the figure
plt.figure(figsize=(10, 6))  # Set the figure width and height
cmap = plt.get_cmap('tab20')  # Get a larger color palette

# Plot the number of fully activated nodes for each k1
for i, k1 in enumerate(k1_values):
    subset = data[data['k1'] == k1]
    plt.plot(subset['p'], subset['Average Fully Activated Nodes'], marker='o', color=cmap(i % cmap.N), label=f'k1 = {k1}')

# Set the title and labels, including k2 and total experiments
plt.title(f'Average Fully Activated Nodes vs. Probability (p)\nk2 = {k2_value}, Total Experiments = {experiments}, Nodes = {n}')
plt.xlabel('Probability (p)')
plt.ylabel('Average Fully Activated Nodes')
plt.xticks(np.arange(0, 1.05, 0.05))  # Set the x-axis ticks

plt.legend(title='k1 values', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust the legend position
plt.grid()
plt.tight_layout()

# Show the figure
plt.show()
