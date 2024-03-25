import matplotlib.pyplot as plt
from collections import defaultdict

def read_and_aggregate_data(file_name):
    """
    Reads data from a given file and aggregates the runtime for each number of processors.
    """
    data = defaultdict(list)
    with open(file_name, 'r') as file:
        for line in file:
            processors, runtime = line.strip().split(',') 
            data[int(processors)].append(float(runtime))
    return {p: sum(data[p]) / len(data[p]) for p in sorted(data)}

# File paths
file_a = 'Assignment 1/Results/bw_10.txt'
file_b = 'Assignment 1/Results/blur_10.txt'
file_c = 'Assignment 1/Results/noise_10.txt'

# Reading and aggregating data from each file
data_a = read_and_aggregate_data(file_a)
data_b = read_and_aggregate_data(file_b)
data_c = read_and_aggregate_data(file_c)

# Plotting
plt.figure(figsize=(10, 6))

for data, color, label in zip([data_a, data_b, data_c], ['r', 'g', 'b'], ['process_to_black_and_white', 'process_blur', 'process_noise']):
    plt.plot(data.keys(), data.values(), marker='o', color=color, label=label)

plt.title('Comparison of image processing techniques average run time with different number of processes')
plt.xlabel('Number of Processes')
plt.ylabel('Average Runtime (seconds)')
plt.legend()
plt.savefig('Assignment 1/Results/function_lineplot.png')

