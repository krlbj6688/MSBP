import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
data = pd.read_csv('with_penultimate_weak_proportion_sigma=3.csv')

# Replace NaN (None) values in k1 with a string "None"
data['k1'] = data['k1'].fillna('None')

# Get unique k1 values
k1_values = data['k1'].unique()

# Extract k2 and total experiments and n from the data
k2_value = data['k2'].unique()[0]  # Assuming k2 is constant across all rows
experiments = data['Total Experiments'].unique()[0]  # Assuming total experiments is constant
n = data['n'].unique()[0]

# Create the figure
plt.figure(figsize=(10, 6))  # Set the figure width and height
cmap = plt.get_cmap('tab20')  # Get a larger color palette

# Plot the average weak activation proportion for each k1
for i, k1 in enumerate(k1_values):
    subset = data[data['k1'] == k1]
    plt.plot(subset['p'], subset['Penultimate Weak Activation Proportion'], marker='o', color=cmap(i % cmap.N), label=f'k1 = {k1}')

# Set the title and labels, including k2 and total experiments
plt.title(f'Average Penultimate Weak Activation Proportion vs. Probability (p)\nk2 = {k2_value}, Experiments = {experiments}, Nodes = {n}')
plt.xlabel('Probability (p)')
plt.ylabel('Average Second Last Weak Activation Proportion')
plt.xticks(np.arange(0, 1.05, 0.05))  # Set the x-axis ticks within the range

plt.legend(title='k1 values', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust the legend position
plt.grid()
plt.tight_layout()

# Show the figure
plt.show()
