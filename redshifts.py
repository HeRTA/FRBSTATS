import fruitbat
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

redshifts = []

idx = 0
for dm_value in dm:
	# Create a Frb Object with DM and Galactic Coordinates
	frb = fruitbat.Frb(dm_value, gl=str(l[idx]), gb=str(b[idx]))
	# Calculate the DM contribution from the Milky Way
	frb.calc_dm_galaxy()
	# Calculate the Redshift of the FRB using the relation from Zhang (2018)
	redshift = float(frb.calc_redshift(method="Zhang2018", cosmology="Planck18"))
	redshifts.append(str(redshift))
	idx += 1

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
		idx = 1
		for row in csv_reader:
			# Append the default text in the row / list
			row.append(redshifts[idx])
			# Add the updated row / list to the output file
			csv_writer.writerow(row)
			idx += 1
