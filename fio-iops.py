import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Process a CSV file.')
parser.add_argument('-i', '--input', type=str, help='The path to the input file')
parser.add_argument('-o', '--output', type=str, help='The path to the output file')
args = parser.parse_args()

# Load the data
df = pd.read_csv(args.input, header=None)

# Remove columns 3, 4, and 5 (Python uses 0-based indexing, so these are columns 2, 3, 4)
df = df.drop(df.columns[[2, 3, 4]], axis=1)

# Rename the remaining columns
df.columns = ['Numbers', 'Values']

# Round down the numbers to the nearest thousand
df['Numbers'] = (df['Numbers'] // 1000) * 1000

# Extract unique values from the 'Numbers' column
unique_numbers = df['Numbers'].unique()

# Create a new dataframe with these unique values as columns
new_df = pd.DataFrame(columns=unique_numbers)

# For each unique number, get the corresponding values and place them in the new dataframe
for num in unique_numbers:
    # Get the values corresponding to the current number
    values = df[df['Numbers'] == num]['Values'].values
    
    # Add these values to the corresponding column in the new dataframe
    new_df[num] = pd.Series(values)

# Keep only the columns that are evenly divisible by 5000
columns_to_keep = [col for col in new_df.columns if col % 5000 == 0]
new_df = new_df[columns_to_keep]

# Save the new dataframe to a CSV file
new_df.to_csv(args.output, index=False)

# Create a line chart
plt.figure(figsize=(10, 6))
for i in range(len(new_df)):
    plt.plot(new_df.columns, new_df.iloc[i])

plt.xlabel('Time In MS Since Start')
plt.ylabel('Row Values')
plt.title('Line Chart')

# Set the vertical axis range based on the data
lowest_value = new_df.min().min() - 30
highest_value = new_df.max().max() + 30
plt.ylim(lowest_value, highest_value)

# plt.legend()  # Do not present a legend
plt.savefig('chart.png')

