import matplotlib.pyplot as plt
from collections import defaultdict

# Reading the data
data_file = 'Assignment 1/Results/scenario_1_10.txt'
data = defaultdict(list)

with open(data_file, 'r') as file:
    for line in file:
        processors, runtime = line.strip().split(
            ',') 
        data[int(processors)].append(float(runtime))

# Aggregating the data
processors = sorted(data.keys())
average_runtimes = [sum(data[p]) / len(data[p]) for p in processors]

# Generating the line graph
plt.figure(figsize=(10, 6))
plt.plot(processors, average_runtimes, marker='o')
plt.title('Processes vs. Average Runtime')
plt.xlabel('Number of Processes')
plt.ylabel('Average Runtime (seconds)')


plt.xticks([i for i in range(3, 13)])
plt.yticks([i for i in range(0, 300, 20)])


# Show the plot
plt.savefig('Assignment 1/Results/scenario_1_test.png')
