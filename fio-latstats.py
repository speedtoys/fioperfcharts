#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the new data and drop unnecessary columns
data_new = pd.read_csv("./latlog_lat.log", sep=",\s*", engine='python', header=None)
data_new.drop([2, 3, 4], axis=1, inplace=True)
data_new.columns = ['Time', 'Value']

# Round down the values in the first column to the nearest thousand
data_new['Time'] = (data_new['Time'] // 1000) * 1000

# Reshape the new data
grouped_data_new = data_new.groupby('Time')['Value'].apply(list)
reshaped_data_new = pd.DataFrame(grouped_data_new).transpose()
reshaped_data_new.columns = reshaped_data_new.columns.astype(int)

# Drop columns not evenly divisible by 10000
cols_to_drop_new = [col for col in reshaped_data_new.columns if col % 10000 != 0]
reshaped_data_new.drop(columns=cols_to_drop_new, inplace=True)

# Convert the values from nanoseconds to microseconds
reshaped_data_new = reshaped_data_new.applymap(lambda x: [val / 1e3 for val in x])

# Calculate the high, low, average, and standard deviation for each 'Time'
high_values = reshaped_data_new.apply(lambda x: max(x[0]))
low_values = reshaped_data_new.apply(lambda x: min(x[0]))
average_values = reshaped_data_new.apply(lambda x: np.mean(x[0]))
std_dev_values = reshaped_data_new.apply(lambda x: np.std(x[0]))

# Convert the 'Time' values from milliseconds to seconds
high_values.index = high_values.index / 1000
low_values.index = low_values.index / 1000
average_values.index = average_values.index / 1000
std_dev_values.index = std_dev_values.index / 1000

# Find the range for the vertical axis
vmin_stats = min(low_values.min(), average_values.min() - std_dev_values.max()) - 100
vmax_stats = max(high_values.max(), average_values.max() + std_dev_values.max()) + 100

# Create the line chart
plt.figure(figsize=(10, 6))

# Plot the high, low, average, and standard deviation as separate lines
plt.plot(high_values.index, high_values, label='High', color='red')
plt.plot(low_values.index, low_values, label='Low', color='blue')
# plt.plot(average_values.index, average_values, label='Average', color='green')
plt.fill_between(average_values.index, average_values - std_dev_values, average_values + std_dev_values, color='gray', alpha=0.5, label='Standard Deviation')

# Set the labels and title
plt.xlabel('Time In Seconds Since Start')
plt.ylabel('Latency (in µS)')
plt.title('Latency Statistics Over Time (in µS)')

# Set the range for the vertical axis
plt.ylim([vmin_stats, vmax_stats])

# Display a legend
plt.legend()

# Save the plot as a PNG file
plt.savefig('latency-statistics.png')

