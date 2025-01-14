import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
data = pd.read_csv('activation_process_1.csv')

# Replace NaN (None) values in k1 with a string "None"
data['k1'] = data['k1'].fillna('None')

# Get unique k1 values
k1_values = data['k1'].unique()

# Extract k2, total experiments, and n from the data
k2_value = data['k2'].unique()[0]  # Assuming k2 is constant across all rows
experiments = data['Total Experiments'].unique()[0]  # Assuming total experiments is constant
n = data['n'].unique()[0]

# Set font sizes for larger text
plt.rcParams.update({'font.size': 10})  # Increase general font size

# Create the figure
plt.figure(figsize=(10, 6))  # Set the figure width and height
cmap = plt.get_cmap('tab20')  # Get a larger color palette

# Plot the First Step Weak Activation Count for each k1
for i, k1 in enumerate(k1_values):
    subset = data[data['k1'] == k1]
    plt.plot(subset['p'], subset['First Step Weak Activation Count'], marker='o', color=cmap(i % cmap.N), label=f'k1 = {k1}')

# Set the title and labels, including k2 and total experiments
plt.title(f'First Step Weak Activation Count vs. Probability (p)\nk2 = {k2_value}, Experiments = {experiments}, Nodes = {n}', fontsize=16)
plt.xlabel('Probability (p)', fontsize=14)
plt.ylabel('First Step Weak Activation Count', fontsize=14)
plt.xticks(np.arange(0, 1.05, 0.05))  # Set the x-axis ticks within the range
plt.yticks(fontsize=12)  # Adjust y-axis tick size

plt.legend(title='k1 values', bbox_to_anchor=(1.05, 1), loc='upper left', title_fontsize=12, fontsize=10)  # Adjust legend font sizes
plt.grid()
plt.tight_layout()

# Show the figure
plt.show()
