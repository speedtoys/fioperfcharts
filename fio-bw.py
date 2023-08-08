import pandas as pd
import matplotlib.pyplot as plt

# Load the data and drop unnecessary columns
data_bw = pd.read_csv("./bwlog_bw.log", sep=",\s*", engine='python', header=None)
data_bw.drop([2, 3, 4], axis=1, inplace=True)
data_bw.columns = ['Time', 'Value']

# Round down the values in the first column to the nearest thousand
data_bw['Time'] = (data_bw['Time'] // 1000) * 1000

# Sum the values for each 'Time'
summed_data_bw = data_bw.groupby('Time')['Value'].sum()

# Drop rows where the time is not evenly divisible by 10000
summed_data_bw = summed_data_bw[summed_data_bw.index % 10000 == 0]

# Find the range for the vertical axis
vmin_bw = summed_data_bw.min() - 100000
vmax_bw = summed_data_bw.max() + 100000

# Create the line chart
plt.figure(figsize=(10, 6))
plt.plot(summed_data_bw.index / 1000, summed_data_bw, marker='o')

# Set the labels and title
plt.xlabel('Time In Seconds Since Start')
plt.ylabel('Throughput GB/s')
plt.title('Throughput Over Time')

# Set the range for the vertical axis
plt.ylim([vmin_bw, vmax_bw])

# Do not display a legend
plt.gca().legend_ = None

# Save the plot as a PNG file
plt.savefig('bandwidth.png')
