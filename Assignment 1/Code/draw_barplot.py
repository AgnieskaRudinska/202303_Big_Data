from collections import defaultdict
import matplotlib.pyplot as plt

# Data
values = []  # Your values here
data_files = ['Assignment 1/Results/bw_10.txt', 'Assignment 1/Results/blur_10.txt', 'Assignment 1/Results/noise_10.txt']
for file in data_files:
    data = defaultdict(list)

    with open(file, 'r') as file:
        for line in file:
            processors, runtime = line.strip().split(',')  # Change ',' to your actual delimiter
            data[int(processors)].append(float(runtime))

    # Step 2: Aggregate the data
    processors = sorted(data.keys())
    average_runtimes = [sum(data[p]) / len(data[p]) for p in processors]
    
    idx = processors.index(12)
    values.append(average_runtimes[idx])
labels = ['process_to_black_and_white', 'process_blur', 'process_noise']  # Labels for each bar

# Create the bar plot
plt.figure(figsize=(8, 6))
plt.bar(labels, values, color=['red', 'green', 'blue'])  # You can customize the colors

# Adding titles and labels
plt.title('Comparison of image processing techniques average run time')
plt.xlabel('Functions')
plt.ylabel('Average run time (seconds)')
plt.xticks(labels)  # Ensures that each bar has a label

# Display the plot
plt.savefig('Assignment 1/Results/function_barplot.png')
