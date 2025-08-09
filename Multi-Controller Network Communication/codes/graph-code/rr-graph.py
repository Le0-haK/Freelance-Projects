import numpy as np
import matplotlib.pyplot as plt

# Data
test_cases = ['Best Case', 'Average Case', 'Worst Case']
request_distribution = [[34, 33, 33], [33.4, 33.3, 33.3], [40, 30, 30]]
load_balancing = [97.0, 99.7, 70.0]

# Set the width of the bars
bar_width = 0.35

# Set position of bar on X axis
r1 = np.arange(len(test_cases))
r2 = [x + bar_width for x in r1]

# Plotting
plt.figure(figsize=(10, 6))

# Request Distribution
for i, dist in enumerate(request_distribution):
    plt.bar(r1[i], dist[0], color='lightblue', width=bar_width/3, edgecolor='grey', label='Host 1' if i == 0 else '', bottom=dist[1]+dist[2])
    plt.bar(r1[i], dist[1], color='skyblue', width=bar_width/3, edgecolor='grey', label='Host 2' if i == 0 else '', bottom=dist[2])
    plt.bar(r1[i], dist[2], color='deepskyblue', width=bar_width/3, edgecolor='grey', label='Host 3' if i == 0 else '')

# Load Balancing
plt.bar(r2, load_balancing, color='lightgreen', width=bar_width, edgecolor='grey', label='Load Balancing (%)')

# Title and labels
plt.title('Test Case Results')
plt.xlabel('Test Cases', fontweight='bold')
plt.ylabel('Percentage', fontweight='bold')
plt.xticks([r + bar_width/2 for r in range(len(test_cases))], test_cases)
plt.grid(axis='y')
plt.legend()

# Show plot
plt.tight_layout()
plt.show()
