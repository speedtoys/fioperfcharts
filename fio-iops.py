#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

# Load the data and drop unnecessary columns
data_iops = pd.read_csv("./iopslog_iops.log", sep=",\s*", engine='python', header=None)
data_iops.drop([2, 3, 4], axis=1, inplace=True)
data_iops.columns = ['Time', 'Value']

# Round down the values in the first column to the nearest thousand
data_iops['Time'] = (data_iops['Time'] // 1000) * 1000

# Sum the values for each 'Time'
summed_data_iops = data_iops.groupby('Time')['Value'].sum()

# Drop rows where the time is not evenly divisible by 5000
summed_data_iops = summed_data_iops[summed_data_iops.index % 5000 == 0]

# Find the range for the vertical axis
vmin_iops = summed_data_iops.min() - 500
vmax_iops = summed_data_iops.max() + 500

# Create the line chart
plt.figure(figsize=(10, 6))
plt.plot(summed_data_iops.index / 1000, summed_data_iops, marker='o')

# Set the labels and title
plt.xlabel('Time In MS Since Start')
plt.ylabel('IOPS')
plt.title('IOPS Over Time')

# Set the range for the vertical axis
plt.ylim([vmin_iops, vmax_iops])

# Do not display a legend
plt.gca().legend_ = None

# Save the plot as a PNG file
plt.savefig('iops.png')

