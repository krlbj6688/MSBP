import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
data = pd.read_csv('activation_process_1.csv')

# Replace NaN (None) values in k1 with a string "None"
data['k1'] = data['k1'].fillna('None')

# Get unique k1 values in the range 13 to 15
#k1_values = [14]
k1_values = [13,14,15]

# Extract k2, total experiments, and n from the data
k2_value = data['k2'].unique()[0]  # Assuming k2 is constant across all rows
experiments = data['Total Experiments'].unique()[0]  # Assuming total experiments is constant
n = data['n'].unique()[0]

# Set font sizes for larger text
plt.rcParams.update({'font.size': 12})  # Set default font size

# Create the figure
plt.figure(figsize=(10, 6))  # Set the figure width and height
cmap = plt.get_cmap('tab20')  # Get a larger color palette

# Plot the average direct full activation ratio for each k1
for i, k1 in enumerate(k1_values):
    subset = data[data['k1'] == k1]
    plt.plot(subset['p'], subset['Average Direct Full Activation Proportion'], marker='o', color=cmap(i % cmap.N),
             label=f'k1 = {k1}')

    # # Add text for each point with iteration step above and first step weak activation count below
    # for j in range(len(subset)):
    #     p_value = subset.iloc[j]['p']
    #     proportion = subset.iloc[j]['Average Direct Full Activation Proportion']
    #
    #     # Display the iteration step rounded to two decimal places above the point
    #     iteration_step = subset.iloc[j]['Average Iterations for Full Activation']
    #     plt.text(p_value, proportion + 0.01, f'{iteration_step:.2f}', ha='center', va='bottom', fontsize=10,
    #              color='blue')
    #
    #     # Display the first step weak activation count below the point
    #     weak_activation_count = subset.iloc[j]['Full Activation Proportion']  # Adjust column name if necessary
    #     plt.text(p_value, proportion - 0.01, f'{weak_activation_count:.2f}', ha='center', va='top', fontsize=10,
    #              color='green')

# Set the title and labels, including k2 and total experiments
plt.title(f'Average Direct Full Activation Proportion vs. Probability (p)\nk2 = {k2_value}, Experiments = {experiments}, Nodes = {n}', fontsize=16)
plt.xlabel('Probability (p)', fontsize=14)
plt.ylabel('Average Direct Full Activation Proportion', fontsize=14)
plt.xticks(np.arange(0, 1.05, 0.05), fontsize=12)  # Set x-axis tick size
plt.yticks(fontsize=12)  # Set y-axis tick size

# Configure legend with larger font sizes
plt.legend(title='k1 values', bbox_to_anchor=(1.05, 1), loc='upper left', title_fontsize=12, fontsize=10)  # Adjust legend font sizes
plt.grid()
plt.tight_layout()

# Show the figure
plt.show()
