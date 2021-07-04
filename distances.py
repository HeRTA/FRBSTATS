import pygedm
from csv import reader, writer

# Load data
# Initiate empty parameter lists
l = []
b = []
dm = []

# Read FRBSTATS CSV catalogue
with open('catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			l.append(row[6])
			b.append(row[7])
			dm.append(row[9])

# Pre-process data (pick out incompatible rows)
idx_mask = set()
for idx, val in enumerate(l):
	try:
		l[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(b):
	try:
		b[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(dm):
	try:
		dm[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del l[idx]
	del b[idx]
	del dm[idx]

distances = []

idx = 0
for dm_value in dm:
	distance, tau_sc = pygedm.dm_to_dist(l[idx], b[idx], dm_value)
	distances.append(str(distance))
	idx += 1

print(l[0], b[0], dm[0], distances[0])
print(l[1], b[1], dm[1], distances[1])
print(l[2], b[2], dm[2], distances[2])

# Open the input_file in read mode and output_file in write mode
with open('catalogue.csv', 'r') as read_obj, open('catalogue_out.csv', 'w', newline='') as write_obj:
	# Create a csv.reader object from the input file object
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		# Create a csv.writer object from the output file object
		csv_writer = writer(write_obj)
		# Read each row of the input csv file as list
		idx = 0
		for row in csv_reader:
			print(row, idx)
			# Append the default text in the row / list
			row.append(distances[idx])
			# Add the updated row / list to the output file
			csv_writer.writerow(row)
			idx += 1
