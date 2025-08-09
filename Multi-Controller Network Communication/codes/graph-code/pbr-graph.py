import matplotlib.pyplot as plt

# Data
test_cases = ['Best Case', 'Average Case', 'Worst Case']
failover_time = [0.619, 2.365, 4.142]
data_consistency = [96.9, 92.5, 90.2]

# Plotting
plt.figure(figsize=(10, 6))

# Failover Time
plt.plot(test_cases, failover_time, marker='o', label='Failover Time (s)')

# Data Consistency
plt.plot(test_cases, data_consistency, marker='s', label='Data Consistency (%)')

# Title and labels
plt.title('Test Case Results')
plt.xlabel('Test Cases')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()
