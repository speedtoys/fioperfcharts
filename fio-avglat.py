#!/usr/bin/python3

import pandas as pd
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
# This must match the value 'log_avg_msec' set in the FIO configuration for sanity checking
cols_to_drop_new = [col for col in reshaped_data_new.columns if col % 10000 != 0]
reshaped_data_new.drop(columns=cols_to_drop_new, inplace=True)

# Delete the conversion (and edit the math required) to get the value you need in the chart
#
# Convert the values from nanoseconds to milliseconds
reshaped_data_new = reshaped_data_new.applymap(lambda x: [val / 1e6 for val in x])

# Convert the values from milliseconds to microseconds
reshaped_data_new = reshaped_data_new.applymap(lambda x: [val * 1e3 for val in x])

# Calculate the average of 'Value' entries for each 'Time'
averages_new_us = reshaped_data_new.apply(lambda x: sum(x[0]) / len(x[0]))

# Convert the 'Time' values from milliseconds to seconds
averages_new_us.index = averages_new_us.index / 1000

# Find the range for the vertical axis
vmin_new_us = averages_new_us.min() - 1000
vmax_new_us = averages_new_us.max() + 1000

# Create the line chart
plt.figure(figsize=(10, 6))
plt.plot(averages_new_us.index, averages_new_us, marker='o')

# Set the labels and title
plt.xlabel('Time In Seconds Since Start')
plt.ylabel('Latency (in µS)')
plt.title('Average Latency Value Over Time (in µS)')

# Set the range for the vertical axis
plt.ylim([vmin_new_us, vmax_new_us])

# Do not display a legend
# plt.legend().remove()

# Save the plot as a PNG file
plt.savefig('avg-latency.png')
