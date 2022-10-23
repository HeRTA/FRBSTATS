import sys
import json
from csv import reader
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

### Set MPL plot parameters
# Selectable SVG text
plt.rcParams['svg.fonttype'] = 'none'

# Use TeX
plt.rcParams['text.usetex'] = True

# Set figsize
plt.rcParams["figure.figsize"] = (24,12)
plt.rcParams["figure.dpi"] = 300

# Set xtick size
plt.rcParams['xtick.major.size'] = 20
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 10
plt.rcParams['xtick.minor.width'] = 2

# Set ytick size
plt.rcParams['ytick.major.size'] = 20
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['ytick.minor.size'] = 10
plt.rcParams['ytick.minor.width'] = 2

# Hide secondary spines
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

repeater = str(sys.argv[1])

### Load data
# Initiate empty parameter lists
with open('../../repeaters.json') as f:
    channels = json.loads(f.read())

parents = []
for parent in range(len(channels[0]['children'])):
        parents.append(channels[0]['children'][parent]['name'])

frb_index = parents.index(repeater)
children = []
for child in range(len(channels[0]['children'][frb_index]['children'])):
	children.append(channels[0]['children'][frb_index]['children'][child]['name'])

frb = [parents[frb_index]] + children

telescope = []
snr = []
mjd = []

# Read FRBSTATS CSV catalogue
with open('../../catalogue.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			if any(burst in row for burst in frb):
				telescope.append(row[3])
				snr.append(row[13])
				mjd.append(row[2])

### Pre-process data
# Pick out incompatible rows
idx_mask = set()

for idx, val in enumerate(telescope):
	if str(val) != '-':
		telescope[idx] = str(val)
	else:
		idx_mask.add(idx)

for idx, val in enumerate(snr):
	try:
		snr[idx] = float(val)
	except ValueError:
		idx_mask.add(idx)

for idx, val in enumerate(mjd):
	try:
		mjd[idx] = float(val)
	except:
		idx_mask.add(idx)

# Dump rows with missing data
for idx in sorted(idx_mask, reverse=True):
	del frb[idx]
	del telescope[idx]
	del snr[idx]
	del mjd[idx]

### Initiate plot
# Apply grid
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)

# Define telescope colors
telescope_clr = {
	'Arecibo': 'orange',
	'ATA': 'darkcyan',
	'ASKAP': 'green',
	'CHIME': 'red',
	'DSA-10': 'violet',
	'Effelsberg': 'aquamarine',
	'FAST': 'cyan',
	'GBT': 'purple',
	'GMRT': 'yellow',
	'SRT': 'olive',
	'Parkes': 'royalblue',
	'Pushchino LPA': 'lightcoral',
	'Stockert': 'brown',
	'UTMOST': 'chocolate',
        'VLA': 'deeppink',
        'WSRT/Apertif': 'steelblue'
}

# Scatter plot
plt.scatter(mjd, snr, c=[telescope_clr[i] for i in telescope], s=500, alpha=0.8, linewidth=2, zorder=10)
plt.plot(mjd, snr, c='black', linestyle='--', linewidth=2, zorder=5)

for tel, clr in telescope_clr.items():
	if tel in telescope:
		plt.plot([],[], marker='o', markersize=25, linestyle='', label=r'$\mathrm{'+tel.replace(' ', r'\ ')+r'}$', c=clr)

# Set axis labels & figure title
plt.xlabel(r'$\mathrm{Modified \ Julian \ Date}$', fontsize=52, labelpad=9)
plt.ylabel(r'$\mathrm{Detection \ S/N}$', fontsize=52, labelpad=12)
plt.title(r'$\mathrm{'+frb[0].replace(' ', r' \ ')+' \ }-\mathrm{ \ Repeater \ Time \ Series}$', fontsize=72, y=1.03)

# Enable legend
plt.legend(bbox_to_anchor=(0.25, 1.0), loc='best', numpoints=1, fontsize=34, framealpha=0.5) #, bbox_to_anchor=(0.215, 1.0, 0., 0.0),

# Set tick size
plt.xticks(fontsize=42, y=-0.005)
plt.yticks(fontsize=42)

plt.tight_layout()

# Save data to a scalable format
plt.savefig(frb[0].lower().replace(' ', '_')+'.svg', format='svg')
plt.savefig(frb[0].lower().replace(' ', '_')+'.pdf')
plt.savefig(frb[0].lower().replace(' ', '_')+'.png')
