import argparse
import os
import pickle

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument('results_file', help='Path to results pickle file.')
parser.add_argument('bins', help='Number of bins for the histogram.', type=int)
args = parser.parse_args()


# Load results
results = pickle.load(open(args.results_file, 'rb'))

results_base_file_name, _ = os.path.splitext(os.path.basename(args.results_file))
output_name_base = os.path.join('results/', results_base_file_name)
os.makedirs('results/', exist_ok=True)

# Create histogram of wait times
fig = plt.figure(figsize=(12, 7))
axes = fig.add_subplot(111)
axes.hist(results['total_wait'], bins=args.bins, edgecolor='black')
axes.set_xlabel('Wait time (frames)')
axes.set_ylabel('Frequency')
axes.set_title('Distribution of wait times at traffic lights')
output_name = output_name_base + 'wait_time.png'
fig.savefig(output_name, bbox_inches='tight')
plt.close(fig)

# Create histogram of travel times
fig = plt.figure(figsize=(12, 7))
axes = fig.add_subplot(111)
axes.hist(results['total_travel'], bins=args.bins, color='red', edgecolor='black')
axes.set_xlabel('Travel time (frames)')
axes.set_ylabel('Frequency')
axes.set_title('Distribution of travel times')
output_name = output_name_base + '_travel_time.png'
fig.savefig(output_name, bbox_inches='tight')
plt.close(fig)

print('Succesfully created distribution plots in results/.')