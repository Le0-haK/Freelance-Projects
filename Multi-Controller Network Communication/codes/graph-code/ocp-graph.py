import matplotlib.pyplot as plt

# Data
test_scenarios = ['Best Case', 'Average Case', 'Worst Case']
convergence_time = [0.01, 0.04, 0.05]
nodes = [11, 16, 30]
controllers = [3, 3, 2]
latency_reduction = [141.47, 267.44, 797.32]

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Test Scenario Results')

# Convergence Time
axs[0, 0].bar(test_scenarios, convergence_time, color='skyblue')
axs[0, 0].set_title('Convergence Time (s)')
axs[0, 0].set_ylabel('Time (s)')

# Nodes and Controllers
axs[0, 1].bar(test_scenarios, nodes, color='lightgreen', label='Nodes')
axs[0, 1].bar(test_scenarios, controllers, color='lightcoral', label='Controllers', bottom=nodes)
axs[0, 1].set_title('Nodes and Controllers')
axs[0, 1].set_ylabel('Count')
axs[0, 1].legend()

# Latency Reduction
axs[1, 0].bar(test_scenarios, latency_reduction, color='salmon')
axs[1, 0].set_title('Latency Reduction (ms)')
axs[1, 0].set_ylabel('Latency Reduction (ms)')

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show plot
plt.show()
