import numpy as np
import matplotlib.pyplot as plt

# Data
test_cases = ['Best Case', 'Average Case', 'Worst Case']
fault_detection = [97.5, 93.4, 88.3]
automatic_failover = [94.2, 90.2, 84.2]

# Set the width of the bars
bar_width = 0.35

# Set position of bar on X axis
r1 = np.arange(len(test_cases))
r2 = [x + bar_width for x in r1]

# Plotting
plt.figure(figsize=(10, 6))

# Fault Detection
plt.bar(r1, fault_detection, color='skyblue', width=bar_width, edgecolor='grey', label='Fault Detection (%)')

# Automatic Failover
plt.bar(r2, automatic_failover, color='lightgreen', width=bar_width, edgecolor='grey', label='Automatic Failover (%)')

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
